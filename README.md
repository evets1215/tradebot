# Trading Bot

Autonomous Claude Code trading agent for Alpaca. Five cron-scheduled cloud
routines run each weekday; all state lives in Git.

## Quick start

1. Copy `env.template` to `.env` and fill in credentials.
2. `bash scripts/alpaca.sh account` — smoke test Alpaca connection.
3. `bash scripts/notify.sh "hello"` — smoke test Slack (or check fallback in `DAILY-SUMMARY.md`).
4. Open Claude Code in this directory and run `/portfolio`.

## Credentials needed

| Var | Purpose |
|-----|---------|
| `ALPACA_API_KEY` | Alpaca trading |
| `ALPACA_SECRET_KEY` | Alpaca trading |
| `PERPLEXITY_API_KEY` | Market research |
| `SLACK_WEBHOOK_URL` | Notifications |
| `SLACK_SIGNING_SECRET` | Verify Slack Approve/Reject clicks |

## Slack trade approval

New buys are approval-gated. The market-open routine creates a pending ticket,
sends Slack Approve/Reject buttons, and stops. The approval service receives
the button click, revalidates the ticket, submits a limit buy, waits for the
fill, places a protective stop, and sends the final Slack status.

Run the approval receiver on a machine Slack can reach:

```sh
python3 scripts/slack_approval_server.py --host 0.0.0.0 --port ${APPROVAL_PORT:-8787}
```

Configure the Slack app Interactivity Request URL to:

```text
https://<your-public-host>/slack/actions
```

Every approval ends in exactly one final status:

- `SUCCESS`: entry filled and protective stop accepted
- `NO TRADE`: not filled, expired, or moved beyond the approved limit
- `FAILED`: rejected/canceled before fill
- `URGENT`: filled but the protective stop was not accepted

## Backtesting

Run the daily-bar swing backtest before promoting rule changes:

```sh
python3 scripts/backtest.py --start 2019-01-01 --end $(date +%Y-%m-%d) --capital 2500 --append
```

Results append to `memory/BACKTEST-RESULTS.md`.

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
