---
description: Run weekly review workflow locally (Fridays)
---

Run the Friday weekly review workflow. Uses local .env for credentials.
Does NOT commit or push — local runs are ad-hoc.

DATE=$(date +%Y-%m-%d)

STEP 1 — Read memory for full week context:
- memory/WEEKLY-REVIEW.md (match existing template exactly)
- ALL this week's entries in memory/TRADE-LOG.md
- ALL this week's entries in memory/RESEARCH-LOG.md
- ALL this week's entries in memory/PENDING-ORDERS.jsonl
- memory/TRADING-STRATEGY.md

STEP 2 — Pull week-end state:
  bash scripts/alpaca.sh account
  bash scripts/alpaca.sh positions

STEP 3 — Compute metrics:
- Starting portfolio (Monday AM equity)
- Ending portfolio (today's equity)
- Week return ($ and %)
- S&P 500 week return: use /finance-market-analysis:yfinance-data (pull SPY
  weekly return); fall back to bash scripts/perplexity.sh if unavailable
- Trades taken (W/L/open), approval funnel, win rate, best/worst trade, profit factor

STEP 4 — Append full review section to memory/WEEKLY-REVIEW.md matching template.

STEP 5 — SEPA watchlist for next week. For 3-5 names showing momentum or
with upcoming catalysts, run /finance-market-analysis:sepa-strategy. List
pass/fail in the review's "Next Week Watchlist" section.
For any position held >2 weeks, run /finance-market-analysis:estimate-analysis
to check analyst revision trend — deteriorating estimates = weakening thesis.

STEP 5b — Strategy changes may be proposed only. Do NOT update core rules
unless there are at least 30 closed trades overall and 10 in the affected setup.

STEP 6 — Send ONE Slack message:
  bash scripts/notify.sh "Week ending MMM DD
Portfolio: \$X (±X% week, ±X% phase)
vs S&P 500: ±X%
Trades: N (W:X / L:Y / open:Z)
Best: SYM +X%   Worst: SYM -X%
One-line takeaway: <...>
Grade: <letter>"
