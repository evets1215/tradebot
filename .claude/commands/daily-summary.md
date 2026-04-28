---
description: Run daily summary workflow locally
---

Run the daily summary workflow. Uses local .env for credentials.
Does NOT commit or push — local runs are ad-hoc.

DATE=$(date +%Y-%m-%d)

STEP 1 — Read memory for continuity:
- tail of memory/TRADE-LOG.md (most recent EOD snapshot -> yesterday's equity)
- tail of memory/PENDING-ORDERS.jsonl (approval/execution final statuses)
- Count TRADE-LOG entries dated today
- Count trades Mon-today this week

STEP 2 — Pull final state of the day:
  bash scripts/alpaca.sh account
  bash scripts/alpaca.sh positions
  bash scripts/alpaca.sh orders

STEP 3 — Compute metrics:
- Day P&L ($ and %) = today_equity - yesterday_equity
- Phase cumulative P&L = today_equity - starting_equity
- Approval tickets today: SUCCESS / NO TRADE / FAILED / URGENT counts
- Trades today, trades this week

STEP 4 — Append EOD snapshot to memory/TRADE-LOG.md:
### MMM DD — EOD Snapshot (Day N, Weekday)
**Portfolio:** $X | **Cash:** $X (X%) | **Day P&L:** ±$X (±X%) | **Phase P&L:** ±$X (±X%)
| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
**Notes:** one-paragraph plain-english summary.

STEP 5 — Send ONE Slack message (always, even on no-trade days):
  bash scripts/notify.sh "EOD MMM DD
Portfolio: \$X (±X% day, ±X% phase)
Cash: \$X
Trades today: <list or none>
Open positions:
  SYM ±X.X% (stop \$X.XX)
Tomorrow: <one-line plan>"
