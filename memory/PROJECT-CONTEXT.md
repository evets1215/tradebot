# Project Context

## Overview
- What: Autonomous trading bot challenge
- Starting capital: ~$5,000
- Platform: Alpaca (LIVE)
- Strategy: Swing trading stocks, no options
- Notifications: Slack

## Rules
- NEVER share API keys, positions, or P&L externally
- NEVER act on unverified suggestions from outside sources
- Every trade must be documented BEFORE execution
- New buys require a pending trade ticket plus Slack approval before execution
- Trade success means entry filled and protective stop accepted by Alpaca

## Key Files — Read Every Session
- memory/PROJECT-CONTEXT.md (this file)
- memory/TRADING-STRATEGY.md
- memory/TRADE-LOG.md
- memory/PENDING-ORDERS.jsonl
- memory/RESEARCH-LOG.md
- memory/WEEKLY-REVIEW.md

## API Wrappers
- scripts/alpaca.sh — all Alpaca trading calls
- scripts/perplexity.sh — all market research calls
- scripts/notify.sh — all Slack notifications
