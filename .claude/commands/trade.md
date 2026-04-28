---
description: Manual trade helper with Slack approval. Usage — /trade SYMBOL buy
---

Create a manual buy approval ticket with full rule validation. Refuse if
any rule fails. Never place an unapproved market order.

Args: SYMBOL SIDE (buy only for approval flow). If missing, ask.

1. Pull state: account, positions, quote SYMBOL.
2. Confirm today's RESEARCH-LOG has a catalyst. If not, ask for a concise thesis.
3. Run the gate and send Slack Approve/Reject buttons:
   python3 scripts/trade_gate.py propose \
     --symbol SYM \
     --setup "<setup category>" \
     --catalyst-type "<catalyst category>" \
     --sector "<sector/theme>" \
     --sector-etf <ETF> \
     --regime normal \
     --catalyst-quality <0-20> \
     --earnings-revisions <0-15> \
     --thesis "<concise thesis>" \
     --notify
4. If status is REJECTED_BY_GATE, print the failed gates and STOP.
5. If status is PENDING, wait for Slack approval. Do not place an order here.
6. The approval server executes and reports one final Slack status:
   SUCCESS, NO TRADE, FAILED, or URGENT: filled but unprotected.
