# Trading Strategy

## Mission
Beat the S&P 500 over the challenge window. Stocks only — no options, ever.

## Capital & Constraints
- Starting capital: ~$2500
- Platform: Alpaca (LIVE)
- Instruments: Stocks ONLY
- PDT limit: 3 day trades per 5 rolling days (account < $25k)

## Core Rules
1. NO OPTIONS — ever
2. Cash may be 0-100%; never force deployment
3. Max 6 positions at a time
4. New buys require a PENDING ticket from `scripts/trade_gate.py`
5. New buys require Slack approval; Claude must not place unapproved buys
6. Buy execution must use a limit order, never a market order
7. SUCCESS = entry filled AND protective stop accepted by Alpaca
8. Max 3 new trades per week
9. Follow sector momentum
10. Max 35% gross exposure to one sector/theme
11. Max 1% account risk per trade, capped at 20% notional
12. Patience > activity

## Entry Checklist
- Trade setup category documented
- Catalyst category documented
- Signal score >= 70, or >= 80 in bad regimes
- Sector in momentum
- ATR/volatility stop documented
- Target/holding period documented

## Buy-Side Gate (all must pass before any order)
- `scripts/trade_gate.py propose ... --notify` produced a PENDING ticket
- Slack approval received for that exact ticket ID
- Revalidation immediately before execution still passes
- Total positions after fill <= 6
- Trades this week <= 3
- Dollar risk <= 1% of equity
- Notional <= 20% of equity
- Position cost <= available cash
- PDT/day-trade state leaves room
- Catalyst documented in today's RESEARCH-LOG
- Instrument is a stock (not an option)
- Live spread <= 0.30%
- 20d average volume >= 1,000,000 shares
- 20d average dollar volume >= $20,000,000

## Setup Categories
- Post-earnings drift
- Analyst revision momentum
- Sector breakout
- Mean reversion after overreaction
- Biotech catalyst continuation
- Macro/commodity-linked trade
- Sympathy trade

## Signal Score
- Relative strength vs SPY and sector ETF: 20
- Volume surge vs 20-day average: 15
- Catalyst quality: 20
- Earnings/revision support: 15
- Technical setup: 15
- Valuation/overextension penalty: -10
- Liquidity/spread penalty: -10

## Sell-Side Rules
- Unrealized loss beyond planned ticket risk: close immediately
- Thesis broken (catalyst invalidated, sector rolling over): close even if not at -7%
- Up >= +20%: tighten trailing stop to 5%
- Up >= +15%: tighten trailing stop to 7%
- Sector with 2 consecutive failed trades: exit all positions in that sector

## Approval & Execution
1. Claude proposes a candidate and runs `scripts/trade_gate.py propose ... --notify`
2. Slack sends Approve/Reject buttons for the exact ticket
3. `scripts/slack_approval_server.py` receives the click
4. `scripts/execute_approved_trade.py approve TICKET_ID` revalidates live quote/account state
5. Executor submits a limit buy, polls fill status, then submits a protective stop
6. Slack final status must be one of: SUCCESS, NO TRADE, FAILED, URGENT
