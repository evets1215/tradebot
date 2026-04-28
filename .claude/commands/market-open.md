---
description: Run market-open execution workflow locally
---

Run the market-open execution workflow. Uses local .env for credentials.
Does NOT commit or push — local runs are ad-hoc.

DATE=$(date +%Y-%m-%d)

STEP 1 — Read memory for today's plan:
- memory/TRADING-STRATEGY.md
- TODAY's entry in memory/RESEARCH-LOG.md (if missing, run pre-market steps inline)
- tail of memory/TRADE-LOG.md (for weekly trade count)

STEP 2 — Re-validate with live data:
  bash scripts/alpaca.sh account
  bash scripts/alpaca.sh positions
  bash scripts/alpaca.sh quote <each planned ticker>

STEP 3 — For each planned BUY candidate, create a Slack approval ticket.
Use exact setup/catalyst fields from today's RESEARCH-LOG:
  python3 scripts/trade_gate.py propose \
    --symbol SYM \
    --setup "Post-earnings drift" \
    --catalyst-type "Earnings" \
    --sector "Technology" \
    --sector-etf XLK \
    --regime normal \
    --catalyst-quality 15 \
    --earnings-revisions 10 \
    --thesis "One concise thesis from RESEARCH-LOG" \
    --notify

STEP 4 — If the ticket is REJECTED_BY_GATE, do NOT trade. Log the skip.

STEP 5 — If the ticket is PENDING, STOP. Do not place a buy here.
Slack Approve/Reject clicks are handled by:
  python3 scripts/slack_approval_server.py

STEP 6 — Final Slack status must be SUCCESS, NO TRADE, FAILED, or
URGENT: filled but unprotected.
