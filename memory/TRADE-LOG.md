# Trade Log

## Day 0 — EOD Snapshot (pre-launch baseline)
**Portfolio:** $10,000.00 | **Cash:** $10,000.00 (100%) | **Day P&L:** $0 | **Phase P&L:** $0

No positions yet. Bot launches tomorrow.

### Apr 25 — EOD Snapshot (Day 1, Saturday)
**Portfolio:** $0.00 | **Cash:** $0.00 (—) | **Day P&L:** n/a | **Phase P&L:** n/a

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Notes:** Market closed (weekend). Alpaca account ACTIVE but reports $0 equity / $0 cash — account is not yet funded. No positions, no orders, no trades today or this week. Day P&L and Phase P&L marked n/a until account is funded; the $10k Day 0 figure is a pre-launch baseline, not an actual balance, so subtracting against $0 would produce a meaningless -100% figure. Action item: confirm funding before market open Monday Apr 27. Once funded, next EOD will set the real starting equity and resume normal P&L tracking.

### Apr 28 — EOD Snapshot (Day 2, Tuesday)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Day P&L:** $0.00 (0.00%) | **Phase P&L:** $0.00 (0.00%)

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Notes:** Account funded with $2,500 (not the originally planned $10k — actual starting equity is $2,500, which becomes the new phase baseline). No positions, no open orders, no trades today, no trades this week. Alpaca last_equity = $2,500 and current equity = $2,500, so Day P&L is a clean $0. Phase P&L resets to $0 vs. funded baseline. No pre-market or midday research log committed for today, so no thesis triggered an entry. Tomorrow: run pre-market routine to identify 1-2 momentum candidates within 20% sizing cap (~$500/position), respecting 3 trades/week and 75-85% deployment targets — but note absolute capital is small, so commission/spread drag matters more; prioritize high-quality setups over filling the cap.

### Apr 29 — EOD Snapshot (Day 3, Wednesday)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Day P&L:** $0.00 (0.00%) | **Phase P&L:** $0.00 (0.00%)

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Notes:** Flat day — no positions opened, no orders placed, no trades today, 0 trades this week. Alpaca equity = last_equity = $2,500 (balance_asof 2026-04-28; account had no activity to roll). Three pre-market research commits today indicate the routine ran but no setup cleared the gate to PENDING ticket / Slack approval — patience > activity per strategy. Cash sits at 100% awaiting a high-quality momentum setup; weekly cap remains 3 trades and we have used 0. Tomorrow (Thu Apr 30): pre-market routine again, focus on candidates flagged in today's RESEARCH-LOG that survive overnight; target 1 entry sized to ≤$500 with hard stop ≥3% below limit, preserving 1% risk cap (~$25 max loss).

### Apr 30 — Market-Open (Day 4)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Trades this week:** 0/3

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Market-open gate results (no tickets created):**
- NVDA $208.18: signal score ~52/75 — REJECTED_BY_GATE (threshold 70); spread $0.05 ✓; SEPA 8/8 ✓; but score below threshold; 20d MA pullback to $196-200 needed for 2:1 R:R + score improvement
- AVGO $405-420: spread $14.55 (3.6%) — REJECTED_BY_GATE (>0.30% spread rule); SEPA fails C4
- AMZN $268.50: spread $2.99 (1.1%) — REJECTED_BY_GATE (>0.30% spread rule); SEPA fails C2/C4

**Decision:** HOLD. All watchlist candidates rejected by gate criteria. GDP +2.2% (benign); PCE data today (elevated ~3.0%). Macro overhang clearing but no setup meets full entry checklist. Next window: post-POWL earnings May 4, post-SU May 5; watch NVDA for pullback to ~$196-200.

### Apr 30 — EOD Snapshot (Day 4, Thursday)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Day P&L:** $0.00 (0.00%) | **Phase P&L:** $0.00 (0.00%)

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Notes:** Fourth consecutive flat day — no positions, no orders placed, 0 trades today, 0 trades this week (cap 3/wk untouched). Alpaca equity = last_equity = $2,500.00 (balance_asof 2026-04-29; account had no activity). Pre-market research correctly called HOLD ahead of 8:30 AM GDP/PCE/ECI binary event; market-open gate confirmed all three watchlist names rejected (NVDA score below 70 threshold; AVGO and AMZN spread > 0.30%). Discipline > activity — sitting on hands through a macro binary with marginal R:R is the correct call given the $2,500 micro-account where commission/spread drag punishes mediocre entries. Tomorrow (Fri May 1): pre-market routine, then weekly review; revisit NVDA on any pullback to $196-200, AVGO if 50MA recrosses 150MA, AMZN if 3-5 day post-earnings consolidation forms above MAs. Goal stays disciplined: 1 high-conviction entry next week within sizing/risk caps, not forced deployment.

### May 1 — Market-Open (Day 5, new week)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Trades this week:** 0/3

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Market-open gate results (no tickets created):**
- NVDA $201.64 ask / $201.32 bid (spread $0.32 = 0.16% ✓): SEPA 8/8 ✓; in ideal entry zone $200-205; signal score ~65-67/75 — REJECTED_BY_GATE (threshold 70); no fresh catalyst; ISM Mfg PMI 10 AM ET pending; revisit on confirmed base in $196-205 or post-ISM pullback
- AVGO $418.06 ask / $394.58 bid: spread $23.48 (5.6%) — REJECTED_BY_GATE (>0.30% spread rule); SEPA fails C4 (50MA < 150MA)
- AMZN: SEPA FAIL (MA150 < MA200; MA50 < MA150/200) — skip; revisit if MA staircase aligns (4-6 weeks)
- POWL: earnings May 4 AHC — blackout window; revisit post-earnings May 5-6 if positive drift setup forms

**Decision:** HOLD. NVDA in ideal R:R zone (R:R ~3.3:1 at $201.64 entry / $187 stop / $250 target) but score ~65-67/75 still below 70 threshold. ISM at 10 AM is sole remaining catalyst — if soft print causes further tech pullback, midday scan will reassess. AVGO spread disqualifying. Cash 100%, weekly cap 0/3. Next high-conviction windows: NVDA post-ISM (midday), POWL post-earnings May 5, OXY post-earnings ~May 8-12.

### May 1 — EOD Snapshot (Day 5, Friday)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Day P&L:** $0.00 (0.00%) | **Phase P&L:** $0.00 (0.00%)

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Notes:** Fifth consecutive flat day closing week 1. No positions, no orders placed, 0 trades today, 0 trades this week (cap 3/3 unused). Alpaca equity = last_equity = $2,500.00 (balance_asof 2026-04-30; no activity to roll). NVDA gapped to $208-211 premarket then sold off through the ideal $200-205 entry zone to $199.50 intraday (ISM Mfg PMI-driven tech weakness); midday scan confirmed R:R ~4.0:1 at $199.60 entry — but score held at ~63-67/75, below the 70 threshold, so no ticket was proposed. AVGO spread 5.6% disqualifying; AMZN failed SEPA MA staircase; POWL earnings blackout May 4 AHC. Week 1 scorecard: 5/5 days flat, 0 trades, 100% cash, score discipline intact — gate doing its job is a feature. Next week (May 4-8): POWL post-earnings May 5-6 if strong beat + gap held; NVDA reassess Mon pre-market if holds $197-205 (caution: POWL binary same day); OXY post-earnings ~May 8-12. Goal: 1 high-conviction entry, ≤$500, hard stop ≥3% below limit, ≤1% account risk.

### May 2 — EOD Snapshot (Day 6, Saturday — non-trading)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Day P&L:** $0.00 (0.00%) | **Phase P&L:** $0.00 (0.00%)

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Notes:** Weekend — markets closed. No positions, no orders, no trades. Alpaca equity = last_equity = $2,500.00 (balance_asof 2026-05-01; no activity). Week 1 ended flat: 5 trading days, 0 trades, 100% cash. Gate discipline intact throughout — every candidate rejected by score threshold (<70) or spread (>0.30%). Week 2 watchlist: POWL post-earnings May 5-6 (reports May 4 AHC), NVDA pre-market Mon if holding $197-205 range, OXY post-earnings ~May 8-12. Target 1 high-conviction entry ≤$500, hard stop ≥3% below limit, ≤1% account risk (~$25 max loss).

### May 3 — EOD Snapshot (Day 7, Sunday — non-trading)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Day P&L:** $0.00 (0.00%) | **Phase P&L:** $0.00 (0.00%)

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Notes:** Weekend — markets closed. No positions, no orders, no trades. Alpaca equity = last_equity = $2,500.00 (balance_asof 2026-05-01; no activity). Week 1 ended 0-for-5 with 100% cash — gate discipline intact. Week 2 begins Mon May 5 (Mon May 4 likely quiet pre-POWL); key catalysts: POWL earnings May 4 AHC (revisit May 5-6 if strong beat), NVDA pre-market Mon if holding $197-205, OXY post-earnings ~May 8-12. Target 1 high-conviction entry ≤$500, ≤1% account risk (~$25 max loss), limit order only.

### May 4 — Market-Open (Day 8, Week 2)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Trades this week:** 0/3

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Market-open gate results (no tickets created):**
- NVDA $202.00 ask / $200.48 bid: spread 0.75% — REJECTED_BY_GATE (>0.30% spread rule); also signal score ~63-67/75 below 70 threshold; distribution volume flag from Apr 30; POWL binary event tonight adds risk
- AVGO $435.00 ask / $420.25 bid: spread 3.4% — REJECTED_BY_GATE (>0.30% spread rule); SEPA C4 still failing (MA50 < MA150)
- OXY $58.94 ask / $58.90 bid: spread 0.07% ✓ — REJECTED_BY_GATE (earnings blackout; reports AHC May 5 tomorrow)
- POWL: REJECTED_BY_GATE (earnings blackout AHC tonight + SEPA C7 fail >25% below 52w high)

**Decision:** HOLD. No entry. All candidates blocked by spread, signal score, or earnings blackout. POWL reports tonight (AHC May 4) — binary event. Potential FOMC meeting May 6-7 adds further uncertainty through mid-week. Next windows: POWL post-earnings reaction May 5-6 (if SEPA qualifies); OXY post-earnings reaction May 6 (reports AHC May 5); NVDA reassess once score ≥70 and spread normalizes.

### May 4 — EOD Snapshot (Day 8, Monday — Week 2)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Day P&L:** $0.00 (0.00%) | **Phase P&L:** $0.00 (0.00%)

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Notes:** First trading day of week 2 closes flat. No positions, no orders placed, 0 trades today, 0 trades this week (cap 3 unused). Alpaca equity = last_equity = $2,500.00 (balance_asof 2026-05-01; no activity to roll over the weekend). Market-open gate ran a 4-name screen (NVDA, AVGO, OXY, POWL) and rejected all: NVDA on spread (0.75%) + signal score (<70) + distribution-volume flag; AVGO on spread (3.4%) + SEPA C4 fail; OXY on earnings blackout (AHC May 5); POWL on earnings blackout AHC tonight + SEPA C7 fail. Macro setup: VIX 16.78, S&P futures +0.07%, XLE/XLK leading sectors; only tier-1 macro this week is NFP Fri May 8 (60K consensus vs 178K prior) — sizable downside binary. Primary catalyst tonight = POWL earnings; potential FOMC meeting May 6-7 adds mid-week uncertainty. Plan tomorrow: pre-market routine, POWL post-reaction SEPA screen (May 5 if strong beat + gap held + spread normalizes), OXY screen post-AHC May 5, NVDA reassess only on consolidation above $197-202 with VDU. No forced deployment; gate discipline intact.

### May 5 — Market-Open (Day 9, Week 2)
**Portfolio:** $2,500.00 | **Cash:** $2,500.00 (100%) | **Trades this week:** 0/3 | **Daytrade count:** 0/3

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|--------|--------|-------|-------|---------|----------------|------|
| —      | —      | —     | —     | —       | —              | —    |

**Pre-open snapshot (~8:53 AM ET):**
- NVDA: last AH quote bid $197.73 / ask $214.85 — stale closing spread; revalidated at open (see below)
- POWL: AH bid ~$232.88 vs prior close ~$275 = ~-15% AH reaction → earnings miss confirmed; SEPA C7 hard fail; removed from watchlist
- OXY: earnings AHC tonight → blackout
- AVGO: SEPA C4 fail unresolved (MA50 < MA150)

**Market-open gate results — live quotes at 9:35 AM ET (no tickets created):**
- NVDA $198.95 ask / $194.82 bid (spread $4.13 = 2.08%): REJECTED_BY_GATE (>0.30% spread; at-open wide; no TradingAgents BUY signal); SEPA 8/8 valid; NVDA +5.8% open driven by AI chip China export easing catalyst
- ETN $410.40 ask / $369.36 bid (spread $41.04 = 10%): REJECTED_BY_GATE (>0.30% spread + earnings blackout; reported BMO today beating estimates); reassess May 6 post-gap drift
- OXY $59.35 ask / $59.32 bid (spread $0.03 = 0.05% ✓): REJECTED_BY_GATE (earnings blackout AHC tonight; no TradingAgents BUY signal); reassess May 6 post-AHC reaction
- POWL: REJECTED_BY_GATE — earnings miss confirmed; SEPA C7 hard fail; removed from active watchlist
- TradingAgents Run 1 (pre-market): 4x HOLD — AMZN, META, GOOGL, VRT (all above ideal zones; no BUY signals)
- TradingAgents Run 2: FAILED (DEEPSEEK_API_KEY not set in environment)

**Decision:** HOLD. No PENDING ticket created; no `trade_gate.py propose` invoked. TradingAgents produced 0 BUY signals; all candidates blocked by spread, blackout, or score threshold. Binary-event density: JOLTS + ISM Services at 10 AM ET today; OXY AHC tonight; FOMC uncertainty through Wed May 7; NFP binary Fri May 8 (60K consensus vs 178K prior). Cash 100%, 0/3 weekly trades. Next windows: ETN and OXY post-earnings reaction May 6; NVDA if spread normalizes + score ≥70. Gate discipline intact.
