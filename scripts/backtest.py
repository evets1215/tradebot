#!/usr/bin/env python3
"""Daily-bar backtest for the approval-gated swing strategy."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import statistics
import subprocess
from dataclasses import dataclass
from typing import Any

from trade_gate import atr14, avg, pct_return, score_from_data


ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULTS = ROOT / "memory" / "BACKTEST-RESULTS.md"


@dataclass
class Position:
    symbol: str
    entry_date: str
    entry: float
    qty: int
    stop: float
    score: int
    hold_days: int = 0


def alpaca(*args: str) -> Any:
    proc = subprocess.run(
        ["bash", str(ROOT / "scripts" / "alpaca.sh"), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout)


def fetch_bars(symbol: str, start: str, end: str) -> list[dict[str, Any]]:
    data = alpaca("bars", symbol, start, end, "1Day")
    return data.get("bars", {}).get(symbol, [])


def load_universe(path: pathlib.Path) -> list[str]:
    return [line.strip().upper() for line in path.read_text().splitlines() if line.strip() and not line.startswith("#")]


def date_key(bar: dict[str, Any]) -> str:
    return str(bar["t"])[:10]


def bar_by_date(bars: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {date_key(bar): bar for bar in bars}


def returns(values: list[float]) -> list[float]:
    return [values[i] / values[i - 1] - 1.0 for i in range(1, len(values)) if values[i - 1] != 0]


def max_drawdown(equity_curve: list[float]) -> float:
    peak = equity_curve[0]
    worst = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        if peak:
            worst = min(worst, value / peak - 1.0)
    return worst


def sharpe(daily_returns: list[float]) -> float:
    if len(daily_returns) < 2:
        return 0.0
    std = statistics.pstdev(daily_returns)
    if std == 0:
        return 0.0
    return (statistics.mean(daily_returns) / std) * (252 ** 0.5)


def run_backtest(args: argparse.Namespace) -> dict[str, Any]:
    universe = load_universe(pathlib.Path(args.universe))
    all_symbols = sorted(set(universe + ["SPY"]))
    bars = {symbol: fetch_bars(symbol, args.start, args.end) for symbol in all_symbols}
    spy = bars["SPY"]
    dates = [date_key(bar) for bar in spy]
    by_date = {symbol: bar_by_date(symbol_bars) for symbol, symbol_bars in bars.items()}

    cash = args.capital
    positions: dict[str, Position] = {}
    trades: list[dict[str, Any]] = []
    equity_curve: list[float] = []

    for index, date in enumerate(dates):
        if index < 170 or index + 1 >= len(dates):
            continue

        # Mark to market at the open of the current day.
        portfolio_value = cash
        for pos in positions.values():
            bar = by_date[pos.symbol].get(date)
            if bar:
                portfolio_value += pos.qty * float(bar["o"])
        equity_curve.append(portfolio_value)

        # Exit first so same-day capital is not reused optimistically.
        for symbol, pos in list(positions.items()):
            bar = by_date[symbol].get(date)
            if not bar:
                continue
            low = float(bar["l"])
            close = float(bar["c"])
            exit_price = None
            reason = ""
            if low <= pos.stop:
                exit_price = pos.stop * (1 - args.slippage_pct)
                reason = "stop"
            elif pos.hold_days >= args.max_hold_days:
                exit_price = close * (1 - args.slippage_pct)
                reason = "max_hold"
            if exit_price is not None:
                cash += pos.qty * exit_price
                pnl = (exit_price - pos.entry) * pos.qty
                trades.append(
                    {
                        "symbol": symbol,
                        "entry_date": pos.entry_date,
                        "exit_date": date,
                        "entry": pos.entry,
                        "exit": exit_price,
                        "qty": pos.qty,
                        "pnl": pnl,
                        "return": exit_price / pos.entry - 1.0,
                        "score": pos.score,
                        "reason": reason,
                    }
                )
                del positions[symbol]
            else:
                pos.hold_days += 1

        # Score candidates using data known at prior close; enter next open.
        if len(positions) >= args.max_positions:
            continue
        candidates: list[tuple[int, str, float, float]] = []
        for symbol in universe:
            if symbol in positions:
                continue
            symbol_history = [by_date[symbol][d] for d in dates[: index + 1] if d in by_date[symbol]]
            spy_history = spy[: index + 1]
            if len(symbol_history) < 160:
                continue
            score, _, _ = score_from_data(
                symbol_history,
                spy_history,
                spy_history,
                args.catalyst_quality,
                args.earnings_revisions,
            )
            if score < args.score_threshold:
                continue
            next_bar = by_date[symbol].get(dates[index + 1])
            if not next_bar:
                continue
            entry = float(next_bar["o"]) * (1 + args.slippage_pct)
            atr = atr14(symbol_history)
            stop = entry - max(2 * atr, entry * args.min_stop_pct)
            risk_per_share = entry - stop
            if risk_per_share <= 0:
                continue
            qty = int(min((portfolio_value * args.risk_pct) / risk_per_share, (portfolio_value * 0.20) / entry))
            if qty <= 0:
                continue
            candidates.append((score, symbol, entry, stop))

        for score, symbol, entry, stop in sorted(candidates, reverse=True):
            if len(positions) >= args.max_positions:
                break
            risk_per_share = entry - stop
            qty = int(min((portfolio_value * args.risk_pct) / risk_per_share, (portfolio_value * 0.20) / entry))
            cost = qty * entry
            if qty <= 0 or cost > cash:
                continue
            cash -= cost
            positions[symbol] = Position(symbol, dates[index + 1], entry, qty, stop, score)

    final_value = cash
    last_date = dates[-1]
    for pos in positions.values():
        bar = by_date[pos.symbol].get(last_date)
        if bar:
            final_value += pos.qty * float(bar["c"])
    equity_curve.append(final_value)

    wins = [trade for trade in trades if trade["pnl"] > 0]
    losses = [trade for trade in trades if trade["pnl"] <= 0]
    gross_win = sum(trade["pnl"] for trade in wins)
    gross_loss = abs(sum(trade["pnl"] for trade in losses))
    spy_start = float(spy[0]["c"])
    spy_end = float(spy[-1]["c"])
    result = {
        "start": args.start,
        "end": args.end,
        "capital": args.capital,
        "final_value": final_value,
        "return": final_value / args.capital - 1.0,
        "spy_return": spy_end / spy_start - 1.0,
        "trades": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(trades) if trades else 0.0,
        "avg_win": avg([trade["pnl"] for trade in wins]),
        "avg_loss": avg([trade["pnl"] for trade in losses]),
        "profit_factor": gross_win / gross_loss if gross_loss else 0.0,
        "max_drawdown": max_drawdown(equity_curve) if equity_curve else 0.0,
        "sharpe": sharpe(returns(equity_curve)),
    }
    return result


def append_results(result: dict[str, Any]) -> None:
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    text = (
        f"\n## {stamp}\n\n"
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| Window | {result['start']} to {result['end']} |\n"
        f"| Start capital | ${result['capital']:.2f} |\n"
        f"| Final value | ${result['final_value']:.2f} |\n"
        f"| Strategy return | {result['return']:.2%} |\n"
        f"| SPY return | {result['spy_return']:.2%} |\n"
        f"| Trades | {result['trades']} |\n"
        f"| Win rate | {result['win_rate']:.2%} |\n"
        f"| Avg win | ${result['avg_win']:.2f} |\n"
        f"| Avg loss | ${result['avg_loss']:.2f} |\n"
        f"| Profit factor | {result['profit_factor']:.2f} |\n"
        f"| Max drawdown | {result['max_drawdown']:.2%} |\n"
        f"| Sharpe | {result['sharpe']:.2f} |\n"
    )
    with RESULTS.open("a") as fh:
        fh.write(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2019-01-01")
    parser.add_argument("--end", default=dt.date.today().isoformat())
    parser.add_argument("--capital", type=float, default=2500.0)
    parser.add_argument("--universe", default=str(ROOT / "config" / "backtest_universe.txt"))
    parser.add_argument("--score-threshold", type=int, default=70)
    parser.add_argument("--risk-pct", type=float, default=0.01)
    parser.add_argument("--slippage-pct", type=float, default=0.0015)
    parser.add_argument("--min-stop-pct", type=float, default=0.03)
    parser.add_argument("--max-hold-days", type=int, default=10)
    parser.add_argument("--max-positions", type=int, default=6)
    parser.add_argument("--catalyst-quality", type=int, default=15)
    parser.add_argument("--earnings-revisions", type=int, default=10)
    parser.add_argument("--append", action="store_true")
    args = parser.parse_args()
    result = run_backtest(args)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.append:
        append_results(result)


if __name__ == "__main__":
    main()
