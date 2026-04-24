---
description: Run midday scan workflow locally
---

Run the midday scan workflow. Uses local .env for credentials.
Does NOT commit or push — local runs are ad-hoc.

DATE=$(date +%Y-%m-%d)

STEP 1 — Read memory:
- memory/TRADING-STRATEGY.md (exit rules)
- tail of memory/TRADE-LOG.md (entries, thesis per position, stops)
- today's memory/RESEARCH-LOG.md entry

STEP 2 — Pull current state:
  bash scripts/alpaca.sh positions
  bash scripts/alpaca.sh orders

STEP 3 — Cut losers immediately. For every position where unrealized_plpc <= -0.07:
  bash scripts/alpaca.sh close SYM
  bash scripts/alpaca.sh cancel ORDER_ID   # cancel its trailing stop
Log to TRADE-LOG: exit price, realized P&L, "cut at -7% per rule".

STEP 4 — Tighten trailing stops on winners:
- Up >= +20% -> trail_percent: "5"
- Up >= +15% -> trail_percent: "7"
Never tighten within 3% of current price. Never move a stop down.

STEP 5 — Thesis check. Cut any position with a broken thesis, even if not at -7%.

STEP 6 — If any position is moving >3% with no obvious cause:
- Run /finance-data-providers:finance-sentiment on that ticker first
- If sentiment shows sharp negative shift or breaking news, treat as thesis broken
- Only fall back to bash scripts/perplexity.sh if sentiment is neutral/unclear
Append addendum to today's RESEARCH-LOG entry if anything actionable is found.

STEP 7 — Notification: only if action was taken.
  bash scripts/notify.sh "<action summary>"
