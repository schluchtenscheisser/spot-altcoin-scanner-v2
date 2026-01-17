# Glossary
Version: v1.0
Language: English
Audience: Developer + GPT

---

## 1. Purpose

This glossary defines the key terms used across:

- spec
- docs
- code
- backtests
- snapshots
- research context

It ensures consistent meaning and eliminates ambiguity for future development.

---

## 2. Core Trading Concepts

**Breakout**  
Price exceeds prior resistance level (e.g. 20–30d high) with volume confirmation.

**Pullback**  
Retracement inside an existing uptrend, followed by continuation.

**Reversal**  
Downtrend → base → reclaim, indicating structural trend transition.

**Trend**  
Directional price behavior measured by HH/HL and moving averages.

**Reclaim**  
Close retakes level/EMA previously lost, often with momentum and/or volume.

**Base**  
Lateral consolidation after drawdown, typically low volatility and volume compression.

**Overextension**  
Price trades significantly above EMAs; fragility and late-stage characteristics.

**Drawdown**  
Decline from ATH to current level, expressed in percent.

---

## 3. Feature Terms

**r_kd**  
k-day return.

**EMA (Exponential Moving Average)**  
Volatility-weighted moving average with higher responsiveness.

**ATR (Average True Range)**  
Volatility measure normalized as percent for comparability.

**Volume SMA**  
Simple moving average of volume.

**Volume Spike**  
Volume relative to SMA; used as conviction proxy.

---

## 4. Scoring Terms

**Setup**  
Trading archetype (breakout / pullback / reversal) with unique logic.

**Score**  
Normalized value [0–100] for candidate ranking.

**Penalty**  
Multiplicative reduction based on contextual flags (e.g. liquidity).

**Flag**  
Boolean marker explaining context/penalties (e.g. late_stage, low_liquidity).

**Components**  
Weighted internal score subparts.

---

## 5. Pipeline Terms

**Cheap Filter**  
Low-cost reduction early in pipeline (e.g. liquidity, market cap).

**Expensive Filter**  
Costly operations (e.g. OHLCV + Features + Scoring) on shortlist only.

**Snapshot**  
Immutable runtime record used for backtests + reproducibility.

**Backtest**  
Forward-return evaluation based on historical snapshots.

**Shortlist**  
Intermediate asset set after filtering but before scoring.

---

## 6. Market Structure Terms

**ATH (All-Time High)**  
Highest historical price.

**MidCaps**  
Market cap range (100M – 3B) in context of this scanner.

**Liquidity**  
Depth + turnover, proxied by quote-volume in this spec.

**Regime**  
Macro environment affecting behavior of setups (BTC/ETH-led).

---

## 7. Data Terms

**OHLCV**  
Open / High / Low / Close / Volume time-series.

**Market Cap**  
Circulating supply × price (CMC source).

**Mapping**  
Binding between exchange symbols and market cap assets.

---

## 8. GPT Collaboration Terms

**Spec**  
Authoritative description of logic + architecture.

**Code Map**  
Structural view of codebase.

**Snapshot (GPT)**  
State handoff capsule for work continuity.

---

## 9. SQL/Modeling Terms (Optional Future)

**Forward Return**  
Return measured at t+k relative to t.

**Tail Risk**  
Lower distribution percentile behavior.

**Rank Monotonicity**  
Expected ranking quality (higher score → better outcomes).

---

## 10. Anti-Confusion Notes

Glossary excludes:

- sentiment terms
- derivatives terms
- portfolio terms

These may join future versions.

---

## End of `glossary.md`