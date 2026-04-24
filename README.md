# Trading Bot

Autonomous Claude Code trading agent for Alpaca. Five cron-scheduled cloud
routines run each weekday; all state lives in Git.

## Quick start

1. Copy `env.template` to `.env` and fill in credentials.
2. `bash scripts/alpaca.sh account` — smoke test Alpaca connection.
3. `bash scripts/notify.sh "hello"` — smoke test Telegram (or check fallback in `DAILY-SUMMARY.md`).
4. Open Claude Code in this directory and run `/portfolio`.

## Credentials needed

| Var | Purpose |
|-----|---------|
| `ALPACA_API_KEY` | Alpaca trading |
| `ALPACA_SECRET_KEY` | Alpaca trading |
| `PERPLEXITY_API_KEY` | Market research |
| `TELEGRAM_BOT_TOKEN` | Notifications |
| `TELEGRAM_CHAT_ID` | Notifications |

## Cloud routines (America/Chicago)

| Routine | Cron | File |
|---------|------|------|
| Pre-market research | `0 6 * * 1-5` | `routines/pre-market.md` |
| Market-open execution | `30 8 * * 1-5` | `routines/market-open.md` |
| Midday scan | `0 12 * * 1-5` | `routines/midday.md` |
| Daily summary | `0 15 * * 1-5` | `routines/daily-summary.md` |
| Weekly review | `0 16 * * 5` | `routines/weekly-review.md` |

See `routines/README.md` for cloud setup instructions.

## Strategy

Swing trading, stocks only, no options. See `memory/TRADING-STRATEGY.md`.
