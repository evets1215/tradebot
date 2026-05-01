# Weekly Review

Friday reviews appended here.
Template for each entry:

## Week ending YYYY-MM-DD

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $X |
| Ending portfolio | $X |
| Week return | ±$X (±X%) |
| S&P 500 week | ±X% |
| Bot vs S&P | ±X% |
| Trades | N (W:X / L:Y / open:Z) |
| Win rate | X% |
| Best trade | SYM +X% |
| Worst trade | SYM -X% |
| Profit factor | X.XX |

### Closed Trades
| Ticker | Entry | Exit | P&L | Notes |
|--------|-------|------|-----|-------|

### Open Positions at Week End
| Ticker | Entry | Close | Unrealized | Stop |
|--------|-------|-------|------------|------|

### What Worked
- ...

### What Didn't Work
- ...

### Key Lessons
- ...

### Adjustments for Next Week
- ...

### Overall Grade: X

---

## Week ending 2026-05-01

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $2,500.00 (Mon Apr 27; funded Tue Apr 28) |
| Ending portfolio | $2,500.00 |
| Week return | $0.00 (0.00%) |
| S&P 500 week | +0.78% (SPY $715.17 → $720.75) |
| Bot vs S&P | -0.78% |
| Trades | 0 (W:0 / L:0 / open:0) |
| Win rate | N/A (no closed trades) |
| Best trade | N/A |
| Worst trade | N/A |
| Profit factor | N/A |

### Closed Trades
| Ticker | Entry | Exit | P&L | Notes |
|--------|-------|------|-----|-------|
| —      | —     | —    | —   | No trades placed this week |

### Open Positions at Week End
| Ticker | Entry | Close | Unrealized | Stop |
|--------|-------|-------|------------|------|
| —      | —     | —     | —          | —    |

### What Worked
- Discipline held: gate correctly rejected all 3 watchlist candidates each day (NVDA score <70; AVGO/AMZN spread >0.30%; POWL earnings blackout)
- Patience through Wed Apr 29 FOMC and Thu Apr 30 GDP/PCE/ECI binary trio — sat in 100% cash through the macro events
- Daily routine ran reliably — pre-market, market-open, midday, EOD all five days, all committed
- Score gate (signal ≥70) prevented chasing NVDA premarket gap to $208-211 May 1 (sub-2:1 R:R)
- Cash preservation 100% — no commission/spread drag on $2,500 micro-account

### What Didn't Work
- 0% week vs SPY +0.78% = trailed benchmark by 0.78pp; bot is not yet in the market
- Watchlist too narrow (3-4 names, mostly XLK) — single-sector dependency leaves no pipeline when XLK names fail score
- NVDA midday May 1: SEPA 8/8 + R:R 4.0:1 at $199.60 was arguably the cleanest setup of the week, blocked solely by signal score 63-67/75 — score gate may be over-rigid for high-quality SEPA setups in a small account
- Earnings-blackout calendar (POWL May 4, SU May 5, OXY ~May 8-12) drained the watchlist; no rotation candidates from non-tech sectors prepped
- Multiple duplicate Apr 29 pre-market entries in RESEARCH-LOG — research routine ran inconsistently

### Key Lessons
- Patience > activity is correctly the default, but a 0% return when SEPA 8/8 + R:R 4:1 setups exist suggests the signal-score component is binding too tight when SEPA + fundamentals are A-grade
- Watchlist breadth matters as much as depth — need 8-10 candidates across 3+ sectors so the gate can find at least 1 actionable name when single names fail
- Earnings-blackout cluster (3 of 4 watchlist names in blackout next week) means the watchlist should rotate weekly to maintain pipeline coverage
- Micro-account cost structure (commission + spread) penalizes mediocre entries — score discipline is correct, but threshold calibration deserves study (do NOT change yet — needs 2+ weeks of evidence)

### Adjustments for Next Week (May 4-8)
- Expand watchlist to 8-10 names across XLK, XLI, XLF, XLE: add ETN, GS, JPM, alongside existing NVDA, POWL, OXY, SU, AVGO
- Pre-market routine to check POWL post-earnings drift May 5-6 (if positive beat + gap-up holds)
- NVDA: re-engage on either (a) confirmed base in $196-205 with score ≥65, OR (b) pullback to 50MA ~$190-192 with R:R ≥4:1
- OXY: prep entry plan post-earnings ~May 8-12 (positive drift candidate, oil tailwind)
- Track: did the score-gate reject of NVDA midday Fri May 1 ($199.60, SEPA 8/8, R:R 4:1) prove correct or not? Mark for observation; if NVDA breaks above $205 next week without us, evidence for threshold review starts to accumulate
- DO NOT update TRADING-STRATEGY.md this week — score-threshold question needs ≥2 weeks of evidence before any rule change

### Next Week Watchlist (SEPA quick-screen run 2026-05-01)
| Ticker | Last | SEPA 7/7 | 52w Off-Hi | Notes |
|--------|------|----------|------------|-------|
| NVDA   | $198.45 | 7/7 PASS (C4 marginal: MA50 $187.15 vs MA150 $186.31) | -8.4% | Score gate primary blocker |
| POWL   | $275.33 | 7/7 PASS | -0.7% | EARNINGS May 4 AHC — blackout; revisit May 5-6 |
| OXY    | $58.72  | 7/7 PASS | -11.4% | Earnings ~May 8-12 — blackout |
| SU     | $67.56  | 7/7 PASS | -1.3% | Earnings May 5 — blackout |
| ETN    | $425.44 | 6/7 (fails C2: MA150 $361.13 < MA200 $361.32 by $0.19, marginal) | -1.7% | Data-center power; SEPA repairs in 1-2 weeks; watch |

### Strategy Doc Changes This Week
- None. Score-threshold and watchlist-breadth observations logged but not yet codified — need ≥2 weeks of evidence before TRADING-STRATEGY.md edits.

### Overall Grade: C
- Discipline: A (zero forced trades, all gate rejections justified)
- Performance: D (0% vs SPY +0.78% = -0.78pp; bot not yet earning)
- Process: B (routines ran, but research log had duplicates; watchlist too narrow)
- Net: C — a "correct nothing" week, but a benchmark-trailing one. Goal next week: 1 high-conviction entry within sizing/risk caps if a clean setup emerges.
