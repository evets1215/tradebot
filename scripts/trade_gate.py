#!/usr/bin/env python3
"""Create approval-gated trade tickets from live Alpaca data."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import pathlib
import subprocess
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
PENDING = ROOT / "memory" / "PENDING-ORDERS.jsonl"


def run_alpaca(*args: str) -> Any:
    proc = subprocess.run(
        ["bash", str(ROOT / "scripts" / "alpaca.sh"), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(f"alpaca {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return json.loads(proc.stdout)


def notify_payload(payload: dict[str, Any]) -> None:
    proc = subprocess.run(
        ["bash", str(ROOT / "scripts" / "notify.sh"), "--json", json.dumps(payload)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip())


def parse_time(value: str) -> dt.datetime:
    normalized = value.replace("Z", "+00:00")
    if "." in normalized:
        head, tail = normalized.split(".", 1)
        frac = tail
        tz = ""
        for marker in ("+", "-"):
            idx = frac.find(marker)
            if idx > 0:
                tz = frac[idx:]
                frac = frac[:idx]
                break
        normalized = head + "." + frac[:6].ljust(6, "0") + tz
    return dt.datetime.fromisoformat(normalized)


def market_bars(symbols: list[str], days: int = 260) -> dict[str, list[dict[str, Any]]]:
    end = dt.datetime.now(dt.timezone.utc).date()
    start = end - dt.timedelta(days=days)
    data = run_alpaca("bars", ",".join(symbols), start.isoformat(), end.isoformat(), "1Day")
    return data.get("bars", {})


def closes(bars: list[dict[str, Any]]) -> list[float]:
    return [float(bar["c"]) for bar in bars if "c" in bar]


def avg(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def atr14(bars: list[dict[str, Any]]) -> float:
    if len(bars) < 15:
        return 0.0
    trs: list[float] = []
    prev_close = float(bars[-15]["c"])
    for bar in bars[-14:]:
        high = float(bar["h"])
        low = float(bar["l"])
        close = float(bar["c"])
        trs.append(max(high - low, abs(high - prev_close), abs(low - prev_close)))
        prev_close = close
    return avg(trs)


def pct_return(values: list[float], lookback: int) -> float:
    if len(values) <= lookback or values[-lookback] == 0:
        return 0.0
    return values[-1] / values[-lookback] - 1.0


def score_from_data(
    symbol_bars: list[dict[str, Any]],
    spy_bars: list[dict[str, Any]],
    sector_bars: list[dict[str, Any]],
    catalyst_quality: int,
    earnings_revisions: int,
) -> tuple[int, dict[str, int], dict[str, float]]:
    sym_close = closes(symbol_bars)
    spy_close = closes(spy_bars)
    sec_close = closes(sector_bars)
    volumes = [float(bar.get("v", 0)) for bar in symbol_bars]

    rel = 0
    sym_20 = pct_return(sym_close, 20)
    spy_20 = pct_return(spy_close, 20)
    sec_20 = pct_return(sec_close, 20)
    if sym_20 > spy_20:
        rel += 10
    if sym_20 > sec_20:
        rel += 10

    vol_score = 0
    avg20 = avg(volumes[-21:-1])
    surge = volumes[-1] / avg20 if avg20 else 0
    if surge >= 1.5:
        vol_score = 15
    elif surge >= 1.2:
        vol_score = 10
    elif surge >= 1.0:
        vol_score = 5

    tech = 0
    ma20 = avg(sym_close[-20:])
    ma50 = avg(sym_close[-50:])
    ma150 = avg(sym_close[-150:])
    last = sym_close[-1] if sym_close else 0
    if last > ma20:
        tech += 5
    if last > ma50:
        tech += 5
    if ma50 > ma150:
        tech += 5

    overextension_penalty = -10 if ma20 and last / ma20 - 1.0 > 0.15 else 0
    components = {
        "relative_strength": rel,
        "volume_surge": vol_score,
        "catalyst_quality": max(0, min(20, catalyst_quality)),
        "earnings_revisions": max(0, min(15, earnings_revisions)),
        "technical_setup": tech,
        "overextension_penalty": overextension_penalty,
        "liquidity_spread_penalty": 0,
    }
    diagnostics = {
        "symbol_return_20d": sym_20,
        "spy_return_20d": spy_20,
        "sector_return_20d": sec_20,
        "volume_surge": surge,
        "ma20": ma20,
        "ma50": ma50,
        "ma150": ma150,
    }
    return sum(components.values()), components, diagnostics


def load_latest_records() -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    if not PENDING.exists():
        return latest
    for line in PENDING.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        latest[record["id"]] = record
    return latest


def append_record(record: dict[str, Any]) -> None:
    PENDING.parent.mkdir(parents=True, exist_ok=True)
    with PENDING.open("a") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def slack_approval_payload(ticket: dict[str, Any]) -> dict[str, Any]:
    text = (
        f"Trade approval requested: {ticket['symbol']} "
        f"{ticket['qty']} @ {ticket['limit_price']:.2f}"
    )
    fields = [
        f"*ID*\n{ticket['id']}",
        f"*Setup*\n{ticket['setup']}",
        f"*Score*\n{ticket['score']}/100",
        f"*Limit*\n${ticket['limit_price']:.2f}",
        f"*Stop*\n${ticket['stop_price']:.2f}",
        f"*Risk*\n${ticket['risk_dollars']:.2f}",
        f"*Spread*\n{ticket['spread_pct'] * 100:.2f}%",
        f"*Expires*\n{ticket['expires_at']}",
    ]
    return {
        "text": text,
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": "Trade Approval Requested"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Buy {ticket['symbol']}*"}},
            {
                "type": "section",
                "fields": [{"type": "mrkdwn", "text": item} for item in fields],
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": ticket["thesis"][:280]}},
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve"},
                        "style": "primary",
                        "action_id": "approve_trade",
                        "value": ticket["id"],
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Reject"},
                        "style": "danger",
                        "action_id": "reject_trade",
                        "value": ticket["id"],
                    },
                ],
            },
        ],
    }


def propose(args: argparse.Namespace) -> None:
    symbol = args.symbol.upper()
    sector_etf = args.sector_etf.upper()
    account = run_alpaca("account")
    asset = run_alpaca("asset", symbol)
    quote_payload = run_alpaca("quote", symbol)
    quote = quote_payload.get("quote", quote_payload)
    bid = float(quote.get("bp") or 0)
    ask = float(quote.get("ap") or 0)
    quote_time = quote.get("t")
    now = dt.datetime.now(dt.timezone.utc)
    created_at = now.isoformat(timespec="seconds")
    expires_at = (now + dt.timedelta(minutes=args.expires_minutes)).isoformat(timespec="seconds")

    gates: list[str] = []
    failures: list[str] = []

    if asset.get("tradable") is not True:
        failures.append("asset is not tradable")
    if asset.get("class") not in ("us_equity", None):
        failures.append("asset is not a US equity")
    if ask < args.min_price:
        failures.append(f"ask below min price: {ask:.2f}")
    if quote_time:
        age = (now - parse_time(quote_time)).total_seconds()
        if age > args.max_quote_age_seconds:
            failures.append(f"quote stale: {age:.0f}s old")
    if bid <= 0 or ask <= 0 or ask < bid:
        failures.append("invalid bid/ask")

    spread_pct = (ask - bid) / ask if ask else 1.0
    if spread_pct > args.max_spread_pct:
        failures.append(f"spread too wide: {spread_pct * 100:.2f}%")
    else:
        gates.append("spread pass")

    bars = market_bars([symbol, "SPY", sector_etf])
    symbol_bars = bars.get(symbol, [])
    spy_bars = bars.get("SPY", [])
    sector_bars = bars.get(sector_etf, spy_bars)
    if len(symbol_bars) < 160 or len(spy_bars) < 160:
        failures.append("not enough historical bars")

    avg_volume20 = avg([float(bar.get("v", 0)) for bar in symbol_bars[-20:]])
    avg_close20 = avg([float(bar.get("c", 0)) for bar in symbol_bars[-20:]])
    avg_dollar_volume20 = avg_volume20 * avg_close20
    if avg_volume20 < args.min_avg_volume:
        failures.append(f"20d avg volume too low: {avg_volume20:.0f}")
    if avg_dollar_volume20 < args.min_avg_dollar_volume:
        failures.append(f"20d avg dollar volume too low: {avg_dollar_volume20:.0f}")

    score, components, diagnostics = score_from_data(
        symbol_bars,
        spy_bars,
        sector_bars,
        args.catalyst_quality,
        args.earnings_revisions,
    )
    if spread_pct > args.max_spread_pct / 2:
        components["liquidity_spread_penalty"] = -10
        score -= 10
    threshold = args.bad_regime_threshold if args.regime in {"bear", "high_vol_chop", "macro_event"} else args.score_threshold
    if score < threshold:
        failures.append(f"score {score} below threshold {threshold}")

    entry = ask
    atr = atr14(symbol_bars)
    stop_distance = max(2 * atr, entry * args.min_stop_pct)
    stop_price = entry - stop_distance
    if stop_price <= 0:
        failures.append("invalid stop price")
    risk_per_share = entry - stop_price
    equity = float(account.get("equity", 0))
    cash = float(account.get("cash", 0))
    risk_budget = equity * args.risk_pct
    qty_by_risk = math.floor(risk_budget / risk_per_share) if risk_per_share > 0 else 0
    qty_by_notional = math.floor((equity * args.max_notional_pct) / (entry * (1 + args.limit_tolerance_pct))) if entry else 0
    qty_by_cash = math.floor(cash / (entry * (1 + args.limit_tolerance_pct))) if entry else 0
    qty = min(qty_by_risk, qty_by_notional, qty_by_cash)
    if args.qty is not None:
        qty = min(qty, args.qty)
    if qty <= 0:
        failures.append("computed quantity is zero")

    limit_price = entry * (1 + args.limit_tolerance_pct)
    risk_dollars = qty * risk_per_share
    if args.sector_exposure_pct > args.max_sector_exposure_pct:
        failures.append(f"sector exposure too high: {args.sector_exposure_pct:.2%}")

    status = "PENDING" if not failures else "REJECTED_BY_GATE"
    ticket = {
        "id": f"TRADE-{now.strftime('%Y-%m-%d')}-{symbol}-{now.strftime('%H%M%S')}",
        "status": status,
        "created_at": created_at,
        "expires_at": expires_at,
        "symbol": symbol,
        "side": "buy",
        "qty": qty,
        "limit_price": round(limit_price, 2),
        "entry_reference_price": round(entry, 4),
        "stop_price": round(stop_price, 2),
        "risk_dollars": round(risk_dollars, 2),
        "risk_pct": round(risk_dollars / equity, 4) if equity else 0,
        "score": score,
        "score_threshold": threshold,
        "score_components": components,
        "setup": args.setup,
        "catalyst_type": args.catalyst_type,
        "sector": args.sector,
        "sector_etf": sector_etf,
        "regime": args.regime,
        "thesis": args.thesis,
        "spread_pct": spread_pct,
        "avg_volume20": round(avg_volume20),
        "avg_dollar_volume20": round(avg_dollar_volume20),
        "atr14": round(atr, 4),
        "diagnostics": diagnostics,
        "gates": gates,
        "failures": failures,
        "events": [{"at": created_at, "status": status, "message": "ticket created"}],
    }
    append_record(ticket)
    print(json.dumps(ticket, indent=2, sort_keys=True))
    if failures:
        return
    if args.notify:
        notify_payload(slack_approval_payload(ticket))


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("propose")
    p.add_argument("--symbol", required=True)
    p.add_argument("--setup", required=True)
    p.add_argument("--catalyst-type", required=True)
    p.add_argument("--sector", required=True)
    p.add_argument("--sector-etf", default="SPY")
    p.add_argument("--regime", default="normal")
    p.add_argument("--thesis", required=True)
    p.add_argument("--catalyst-quality", type=int, required=True)
    p.add_argument("--earnings-revisions", type=int, required=True)
    p.add_argument("--qty", type=int)
    p.add_argument("--notify", action="store_true")
    p.add_argument("--expires-minutes", type=int, default=20)
    p.add_argument("--score-threshold", type=int, default=70)
    p.add_argument("--bad-regime-threshold", type=int, default=80)
    p.add_argument("--risk-pct", type=float, default=0.01)
    p.add_argument("--max-notional-pct", type=float, default=0.20)
    p.add_argument("--limit-tolerance-pct", type=float, default=0.0015)
    p.add_argument("--min-stop-pct", type=float, default=0.03)
    p.add_argument("--max-spread-pct", type=float, default=0.003)
    p.add_argument("--min-price", type=float, default=5.0)
    p.add_argument("--min-avg-volume", type=float, default=1_000_000)
    p.add_argument("--min-avg-dollar-volume", type=float, default=20_000_000)
    p.add_argument("--max-sector-exposure-pct", type=float, default=0.35)
    p.add_argument("--sector-exposure-pct", type=float, default=0.0)
    p.add_argument("--max-quote-age-seconds", type=int, default=900)
    p.set_defaults(func=propose)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
