# GPT Snapshot - 2026-01-17

## Status: Phase 3 Complete - Data Layer Finished

---

## ✅ COMPLETED

### Phase 1: Foundation (Utils + Config)
- `scanner/utils/logging_utils.py` - Logging mit Rotation
- `scanner/utils/time_utils.py` - UTC Zeit-Funktionen
- `scanner/utils/io_utils.py` - Datei I/O + Caching
- `scanner/config.py` - Config-Loading mit Validation
- `requirements.txt` - Dependencies erweitert

### Phase 2: Data Clients
- `scanner/clients/mexc_client.py` - MEXC API (Universe, Tickers, Klines)
  - 1837 USDT Spot Pairs
  - Rate-limit handling
  - Caching-System
- `scanner/clients/marketcap_client.py` - CMC API (Market Cap)
  - 5000 Listings
  - Symbol-Map-Builder
  - Collision-Detection

### Phase 3: Mapping Layer
- `scanner/clients/mapping.py` - MEXC ↔ CMC Mapping
  - 88.4% success rate (1624/1837)
  - Confidence scoring
  - Override-System
  - Reports (unmapped, collisions, stats)

---

## 🔄 IN PROGRESS

None - Clean break point

---

## 📋 NEXT STEPS (Phase 4: Pipeline)

### Priority Order:
1. **scanner/pipeline/filters.py** (30min)
   - MidCap filter (100M-3B)
   - Liquidity filter (min volume)
   - Exclusions (stables, wrapped, leveraged)
   
2. **scanner/pipeline/shortlist.py** (15min)
   - Cheap-Pass (Top N by volume)
   - Reduce universe to shortlist
   
3. **scanner/pipeline/ohlcv.py** (20min)
   - Fetch OHLCV for shortlist only
   - 1d + 4h data
   - Caching per symbol
   
4. **scanner/pipeline/features.py** (45min)
   - Feature-Engine (1d + 4h)
   - EMA20/50, ATR, Returns, Volume, HH/HL
   - Drawdown, Breakout-Dist, Base-Detection

**Estimated time: 1.5-2h**

---

## ⚠️ OPEN ISSUES

### Minor:
- `config/mapping_overrides.json` hat ungültiges Format
  - **Fix:** Ersetze mit `{}`
  - **Status:** Funktioniert trotzdem (leere Overrides)

### To Decide:
- Wann Feature-Branch-Workflow starten?
  - **Recommendation:** Nach Phase 4 (Pipeline fertig)
  - **Reason:** MVP-Core dann komplett

---

## 🔧 TECHNICAL DETAILS

### API Keys Required:
- `CMC_API_KEY` - CoinMarketCap (Free Tier)
  - Set via: `export CMC_API_KEY='...'`
  - Currently configured in Codespaces

### Cache Strategy:
- Location: `data/raw/YYYY-MM-DD/`
- Files:
  - `mexc_exchange_info.json`
  - `mexc_24h_tickers.json`
  - `mexc_klines_{SYMBOL}_{INTERVAL}.json`
  - `cmc_listings_start1_limit5000.json`
- Invalidation: Daily (auto)

### Run Modes:
- `standard` - Full pipeline (default)
- `fast` - Use cache only
- `offline` - No API calls
- `backtest` - Evaluation mode

---

## 📊 STATISTICS

### Mapping Results:
- Total MEXC Symbols: 1837
- Mapped to CMC: 1624 (88.4%)
- Unmapped: 213 (11.6%)
- Collisions: 0
- Overrides Used: 0

### Confidence Breakdown:
- High: 1624
- Medium: 0
- Low: 0
- None: 213

### Unmapped Examples:
- AMPED, REFACTA, CARFI (not in CMC top 5000)

---

## 🎯 PROJECT CONTEXT (Important!)

### Trading Setup:
- Exchange: MEXC Spot only
- Quote: USDT only
- Market Cap: 100M - 3B (MidCaps)
- Horizon: Days to few weeks
- Goal: 3 separate setup scores

### Setup Types:
1. **Breakout** - Range break + volume
2. **Pullback** - Trend continuation
3. **Reversal** - Downtrend → Base → Reclaim (PRIORITY!)

### Example Target:
- Humanity Protocol (H) in December
- Drawdown → Base → 3x move
- This is the PRIMARY use case!

---

## 🚫 ANTI-FEATURES (Do NOT implement)

- No global/combined score
- No ML/AI predictions (v1)
- No news/sentiment (v1)
- No futures/leverage
- No auto-trading/execution (v1)

---

## 💡 LESSONS LEARNED (From old prototype)

### Critical Success Factors:
1. **Mapping FIRST** - Symbol collisions killed old version
2. **Setup Separation** - Never mix Breakout/Pullback/Reversal
3. **Cheap→Expensive** - Rate-limits are real
4. **Snapshots** - Backtests need deterministic data

### Old Problems (AVOID!):
- Global score mixed everything → unusable
- Mapping was symbol-only → collisions
- No caching → rate-limit hell
- Feature/Scoring mixed → unmaintainable

---

## 🔗 KEY DOCUMENTS

All specs in `/docs`:
- `spec.md` - Master technical spec
- `scoring.md` - Breakout/Pullback/Reversal details
- `features.md` - Feature-Engine spec
- `mapping.md` - Mapping layer spec
- `pipeline.md` - Pipeline flow
- `context.md` - Trading context (German)
- `lessons_learned.md` - Prototype insights (German)

---

## 🐛 KNOWN BUGS

None currently

---

## ✅ QUALITY CHECKS PASSED

- [x] MEXC Universe loading (1837 pairs)
- [x] CMC Listings loading (5000 coins)
- [x] Mapping success rate >85%
- [x] Caching works (file-based, daily)
- [x] Rate-limit handling (retry + backoff)
- [x] Reports generated (unmapped, stats)
- [x] Config loading (YAML + ENV overrides)
- [x] Logging (file + console)

---

## 📝 NOTES FOR NEXT SESSION

### Start with:
1. Fix `config/mapping_overrides.json` (set to `{}`)
2. Read this snapshot completely
3. Check if cache is stale (delete `data/raw/*` if needed)
4. Start Phase 4 with `filters.py`

### Development Style:
- User works in GitHub Web + Codespaces
- Not a developer (needs full code + instructions)
- Uses `&&` command chains for efficiency
- Prefers test files over inline Python commands

### Git Workflow:
- Currently: Direct commits to main
- Future: Feature branches after Phase 4
- Clean commits with descriptive messages

---

## 🎉 ACHIEVEMENTS TODAY

- 3 Phases completed in ~2h
- All data sources working
- Clean architecture (no tech debt)
- Ready for Pipeline implementation

---

## End of Snapshot
