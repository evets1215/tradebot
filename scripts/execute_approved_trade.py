#!/usr/bin/env python3
"""Approve/reject a pending ticket and report final execution state."""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import json
import pathlib
import subprocess
import sys
import time
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
PENDING = ROOT / "memory" / "PENDING-ORDERS.jsonl"
TRADE_LOG = ROOT / "memory" / "TRADE-LOG.md"
LOCKFILE = ROOT / "memory" / ".approval.lock"


def git(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def git_pull() -> None:
    code, _, err = git("pull", "--rebase", "origin", "main")
    if code != 0:
        notify(f"WARNING: git pull failed before approval\n{err.strip() or 'unknown'}")


def git_commit_push(message: str) -> None:
    git("add", "memory/PENDING-ORDERS.jsonl", "memory/TRADE-LOG.md")
    code, _, _ = git("diff", "--cached", "--quiet")
    if code == 0:
        return  # nothing staged
    code, _, err = git("commit", "-m", message)
    if code != 0:
        notify(f"WARNING: git commit failed\n{err.strip() or 'unknown'}")
        return
    code, _, err = git("push", "origin", "main")
    if code == 0:
        return
    git("pull", "--rebase", "origin", "main")
    code, _, err = git("push", "origin", "main")
    if code != 0:
        notify(f"WARNING: git push failed after retry\n{err.strip() or 'unknown'}")


@contextlib.contextmanager
def approval_lock():
    LOCKFILE.parent.mkdir(parents=True, exist_ok=True)
    with LOCKFILE.open("w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def run(cmd: list[str], *, json_out: bool = True) -> Any:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    if json_out:
        return json.loads(proc.stdout)
    return proc.stdout


def alpaca(*args: str) -> Any:
    return run(["bash", str(ROOT / "scripts" / "alpaca.sh"), *args])


def notify(message: str) -> None:
    run(["bash", str(ROOT / "scripts" / "notify.sh"), message], json_out=False)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


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


def records_by_id() -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    if not PENDING.exists():
        return latest
    for line in PENDING.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        latest[record["id"]] = record
    return latest


def append_record(ticket: dict[str, Any], status: str, message: str, **extra: Any) -> dict[str, Any]:
    updated = dict(ticket)
    updated.update(extra)
    updated["status"] = status
    updated.setdefault("events", [])
    updated["events"] = list(updated["events"]) + [{"at": now_iso(), "status": status, "message": message}]
    with PENDING.open("a") as fh:
        fh.write(json.dumps(updated, sort_keys=True) + "\n")
    return updated


def load_ticket(ticket_id: str) -> dict[str, Any]:
    ticket = records_by_id().get(ticket_id)
    if not ticket:
        raise SystemExit(f"ticket not found: {ticket_id}")
    return ticket


def poll_order(order_id: str, seconds: int) -> dict[str, Any]:
    deadline = time.time() + seconds
    order = alpaca("order-status", order_id)
    while time.time() < deadline:
        order = alpaca("order-status", order_id)
        if order.get("status") in {"filled", "canceled", "expired", "rejected"}:
            return order
        time.sleep(5)
    return order


def log_trade(ticket: dict[str, Any], fill: dict[str, Any], stop: dict[str, Any]) -> None:
    fill_price = float(fill.get("filled_avg_price") or ticket["limit_price"])
    today = dt.datetime.now().strftime("%b %d")
    line = (
        f"\n### {today} - Approved Entry {ticket['id']}\n"
        f"**Trade:** BUY {ticket['qty']} {ticket['symbol']} @ ${fill_price:.2f} | "
        f"Stop: ${ticket['stop_price']:.2f} | Score: {ticket['score']}/100 | "
        f"Setup: {ticket['setup']} | Catalyst: {ticket['catalyst_type']}\n"
        f"**Thesis:** {ticket['thesis']}\n"
        f"**Protection:** Stop order {stop.get('id', 'unknown')} status {stop.get('status', 'unknown')}.\n"
    )
    with TRADE_LOG.open("a") as fh:
        fh.write(line)


def reject(args: argparse.Namespace) -> None:
    with approval_lock():
        git_pull()
        try:
            _reject_inner(args)
        finally:
            git_commit_push(f"trade {args.ticket_id} rejected")


def _reject_inner(args: argparse.Namespace) -> None:
    ticket = load_ticket(args.ticket_id)
    if ticket["status"] not in {"PENDING", "APPROVED"}:
        notify(f"Reject ignored: {args.ticket_id} is already {ticket['status']}.")
        return
    append_record(ticket, "REJECTED", f"rejected by {args.approver}", approver=args.approver)
    notify(f"Rejected by {args.approver}\n{args.ticket_id}\nNo order submitted.")


def approve(args: argparse.Namespace) -> None:
    with approval_lock():
        git_pull()
        try:
            _approve_inner(args)
        finally:
            git_commit_push(f"trade {args.ticket_id} approval flow")


def _approve_inner(args: argparse.Namespace) -> None:
    ticket = load_ticket(args.ticket_id)
    if ticket["status"] != "PENDING":
        notify(f"Approval ignored: {args.ticket_id} is already {ticket['status']}.")
        return

    now = dt.datetime.now(dt.timezone.utc)
    if parse_time(ticket["expires_at"]) < now:
        append_record(ticket, "EXPIRED", "approval arrived after expiration", approver=args.approver)
        notify(f"NO TRADE: approval expired\n{args.ticket_id}\nNo order submitted.")
        return

    quote_payload = alpaca("quote", ticket["symbol"])
    quote = quote_payload.get("quote", quote_payload)
    ask = float(quote.get("ap") or 0)
    if ask <= 0 or ask > float(ticket["limit_price"]):
        append_record(
            ticket,
            "NO_TRADE",
            "current ask exceeded approved limit",
            approver=args.approver,
            current_ask=ask,
        )
        notify(
            f"NO TRADE: ask moved beyond approved limit\n"
            f"{ticket['symbol']} current ask ${ask:.2f} > limit ${ticket['limit_price']:.2f}"
        )
        return

    ticket = append_record(ticket, "APPROVED", f"approved by {args.approver}", approver=args.approver)
    notify(
        f"Approved by {args.approver}\n{ticket['id']}\n"
        f"Submitting limit buy: {ticket['symbol']} {ticket['qty']} @ ${ticket['limit_price']:.2f}"
    )

    order_body = {
        "symbol": ticket["symbol"],
        "qty": str(ticket["qty"]),
        "side": "buy",
        "type": "limit",
        "limit_price": f"{ticket['limit_price']:.2f}",
        "time_in_force": "day",
        "client_order_id": ticket["id"],
    }
    try:
        buy_order = alpaca("order", json.dumps(order_body))
    except RuntimeError as exc:
        append_record(ticket, "FAILED", f"buy order rejected: {exc}", order_body=order_body)
        notify(f"FAILED: buy order rejected\n{ticket['id']}\n{exc}")
        return

    ticket = append_record(
        ticket,
        "SUBMITTED",
        "buy limit submitted",
        order_id=buy_order.get("id"),
        order_body=order_body,
    )
    notify(f"Order submitted\n{ticket['symbol']} buy limit\nOrder ID: {buy_order.get('id')}\nWaiting for fill...")

    fill = poll_order(buy_order["id"], args.fill_timeout_seconds)
    status = fill.get("status")
    filled_qty = float(fill.get("filled_qty") or 0)
    if status != "filled":
        try:
            alpaca("cancel", buy_order["id"])
        except RuntimeError:
            pass
        append_record(ticket, "NO_TRADE", f"buy order not filled: {status}", final_order=fill)
        notify(f"NO TRADE: limit buy not filled\n{ticket['id']}\nFinal status: {status}\nNo position opened.")
        return
    if filled_qty != float(ticket["qty"]):
        append_record(ticket, "PARTIAL_FILL", "partial fill requires manual review", final_order=fill)
        notify(
            f"URGENT: partial fill\n{ticket['symbol']} filled {filled_qty} of {ticket['qty']}\n"
            f"Manual review required."
        )
        return

    avg_fill = float(fill.get("filled_avg_price") or ticket["limit_price"])
    notify(
        f"Entry filled\n{ticket['symbol']} {ticket['qty']} shares\n"
        f"Avg fill: ${avg_fill:.2f}\nNow placing protective stop..."
    )

    stop_body = {
        "symbol": ticket["symbol"],
        "qty": str(ticket["qty"]),
        "side": "sell",
        "type": "stop",
        "stop_price": f"{ticket['stop_price']:.2f}",
        "time_in_force": "gtc",
        "client_order_id": f"{ticket['id']}-STOP",
    }
    try:
        stop_order = alpaca("order", json.dumps(stop_body))
    except RuntimeError as exc:
        append_record(ticket, "UNPROTECTED_POSITION", f"stop rejected: {exc}", final_order=fill)
        notify(
            f"URGENT: Entry filled but stop failed\n"
            f"{ticket['symbol']} {ticket['qty']} @ ${avg_fill:.2f}\n"
            f"Stop rejected: {exc}\nStatus: UNPROTECTED POSITION"
        )
        return

    stop_status = stop_order.get("status", "unknown")
    if stop_status in {"rejected", "canceled", "expired"}:
        append_record(
            ticket,
            "UNPROTECTED_POSITION",
            f"stop order status {stop_status}",
            final_order=fill,
            stop_order=stop_order,
        )
        notify(
            f"URGENT: Entry filled but stop is not live\n"
            f"{ticket['symbol']} {ticket['qty']} @ ${avg_fill:.2f}\n"
            f"Stop status: {stop_status}\nStatus: UNPROTECTED POSITION"
        )
        return

    ticket = append_record(
        ticket,
        "SUCCESS",
        "entry filled and protective stop accepted",
        final_order=fill,
        stop_order=stop_order,
    )
    log_trade(ticket, fill, stop_order)
    notify(
        f"SUCCESS: trade live and protected\n"
        f"{ticket['symbol']} {ticket['qty']} shares\n"
        f"Entry: ${avg_fill:.2f}\nStop: ${ticket['stop_price']:.2f}\n"
        f"Stop order: {stop_order.get('id')}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("approve")
    a.add_argument("ticket_id")
    a.add_argument("--approver", default="slack")
    a.add_argument("--fill-timeout-seconds", type=int, default=120)
    a.set_defaults(func=approve)
    r = sub.add_parser("reject")
    r.add_argument("ticket_id")
    r.add_argument("--approver", default="slack")
    r.set_defaults(func=reject)
    args = parser.parse_args()
    try:
        args.func(args)
    except RuntimeError as exc:
        notify(f"FAILED: execution error\n{getattr(args, 'ticket_id', 'unknown')}\n{exc}")
        raise


if __name__ == "__main__":
    main()
