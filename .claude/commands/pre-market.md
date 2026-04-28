---
description: Run pre-market research workflow locally
---

Run the pre-market research workflow. Uses local .env for credentials.
Does NOT commit or push — local runs are ad-hoc.

DATE=$(date +%Y-%m-%d)

STEP 1 — Read memory for context:
- memory/TRADING-STRATEGY.md
- tail of memory/TRADE-LOG.md
- tail of memory/RESEARCH-LOG.md

STEP 2 — Pull live account state:
  bash scripts/alpaca.sh account
  bash scripts/alpaca.sh positions
  bash scripts/alpaca.sh orders

STEP 3 — Research market context. Use structured skills first; fall back to
bash scripts/perplexity.sh "<query>" only for items not covered:
- Macro: perplexity "WTI and Brent oil price right now"
- Futures: perplexity "S&P 500 futures premarket today"
- VIX: perplexity "VIX level today"
- Economic calendar: perplexity "Economic calendar today CPI PPI FOMC jobs data"
- Sector momentum: use /finance-market-analysis:yfinance-data to pull
  week/month returns for SPY sector ETFs (XLK, XLV, XLE, XLF, XLI, XLY, XLP, XLU, XLB, XLRE)
- Earnings today: use /finance-market-analysis:earnings-preview for any ticker
  reporting before open that overlaps your watchlist or holdings
- Sentiment on held tickers: use /finance-data-providers:finance-sentiment
  for each currently-held symbol; flag any with sharply negative sentiment shift
- Unusual moves on held tickers: use /finance-social-readers:twitter-reader
  to search cashtag (e.g. $SYM) only if sentiment flags something unusual
If Perplexity exits 3, fall back to native WebSearch and note the fallback.

STEP 4 — SEPA screen for new ideas. For 2-3 watchlist candidates with
recent momentum or a specific catalyst, run /finance-market-analysis:sepa-strategy.
Only advance a name to a trade idea if it passes Minervini trend template
(Stage 2: price > 150MA > 200MA, 200MA trending up, RS > 70).

STEP 5 — Write a dated entry to memory/RESEARCH-LOG.md:
- Account snapshot (equity, cash, buying power, daytrade count)
- Market context (oil, indices, VIX, sector leaders/laggards, today's releases)
- Sentiment summary for held tickers (flag any red)
- 2-3 actionable trade ideas WITH:
  ticker, setup category, catalyst type, sector/theme, sector ETF,
  regime, catalyst quality score (0-20), earnings/revisions score (0-15),
  thesis, entry reference, ATR/volatility stop, target, expected holding period
- Risk factors for the day
- Decision: trade or HOLD (default HOLD — patience > activity)

STEP 6 — Notification: silent unless urgent.
  bash scripts/notify.sh "<one line>"
