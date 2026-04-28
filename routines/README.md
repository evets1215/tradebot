# Cloud Routines

Five Claude Code cloud routines fire each weekday. All times America/Chicago.

| Routine | Cron | Purpose |
|---------|------|---------|
| `pre-market.md` | `0 6 * * 1-5` | Research catalysts, write trade ideas |
| `market-open.md` | `30 8 * * 1-5` | Create approval tickets (no direct buys) |
| `midday.md` | `0 12 * * 1-5` | Cut losers, tighten stops on winners |
| `daily-summary.md` | `0 15 * * 1-5` | EOD snapshot + Slack recap |
| `weekly-review.md` | `0 16 * * 5` | Weekly stats, grade, strategy update |

## Setup (do once per routine)

1. Claude Code cloud → Routines → New Routine
2. Name it (e.g. "Trading bot pre-market")
3. Select this repo, branch: main
4. Add environment variables:
   - `ALPACA_API_KEY`
   - `ALPACA_SECRET_KEY`
   - `ALPACA_ENDPOINT` (optional; defaults to live URL)
   - `ALPACA_DATA_ENDPOINT` (optional)
   - `PERPLEXITY_API_KEY`
   - `PERPLEXITY_MODEL` (optional; defaults to sonar)
   - `SLACK_WEBHOOK_URL`
   - `SLACK_SIGNING_SECRET` (approval receiver only)
5. Toggle **"Allow unrestricted branch pushes"** ON — without this, git push silently fails
6. Set cron schedule and timezone (America/Chicago)
7. Paste the contents of the relevant `*.md` file verbatim into the prompt field
8. Save, then hit **"Run now"** once to verify before relying on the schedule

## Approval server (separate from cloud routines)

`market-open` only creates PENDING tickets and posts Slack approve/reject
buttons — it never places a buy. Approvals are processed by
`scripts/slack_approval_server.py`, which must run on a host Slack can
reach (laptop with tunnel, or a small VPS). It is NOT a cloud routine
and must NOT be invoked from one (one-shot processes can't host an HTTP
listener).

Git sync: `execute_approved_trade.py` does `git pull --rebase origin main`
before reading the ticket and `git commit && git push origin main` after
writing outcomes (under an fcntl lock). Cloud routines see final
SUCCESS / NO TRADE / FAILED / URGENT statuses on their next clone. If
push fails, a Slack WARNING is sent — daily-summary still falls back to
deriving outcomes from live Alpaca state, so the report is never wrong.

## Common failure modes

| Symptom | Fix |
|---------|-----|
| Clone fails | Install Claude GitHub App, grant access to this repo |
| `git push` fails silently | Enable "Allow unrestricted branch pushes" |
| `ALPACA_API_KEY not set` | Add var in routine config (not in .env) |
| Agent creates .env anyway | Re-paste prompt verbatim (the DO NOT block was lost) |
| Memory missing next run | Previous run didn't commit — check git log, re-verify STEP N |
| Slack message not received | Check SLACK_WEBHOOK_URL in routine config |
| Slack buttons do nothing | Run `scripts/slack_approval_server.py` and configure Slack Interactivity Request URL |
