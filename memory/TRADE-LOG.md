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
