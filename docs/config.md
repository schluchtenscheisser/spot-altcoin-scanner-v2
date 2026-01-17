# Configuration Specification
Version: v1.0  
Language: English  
Audience: Developer + GPT

---

## 1. Purpose

This document specifies the configurable parameters for the scanner.  
Configuration controls:

- pipeline behavior
- thresholds
- lookbacks
- penalties
- scoring weights
- run modes
- data source usage

Config must be:

- explicit
- deterministic
- versioned
- snapshot-captured

Config changes **affect backtest compatibility** and therefore must increment version.

---

## 2. Configuration Model

Configuration is stored as:

- `config.yml` (primary)
- environment variables (overrides)
- CLI arguments (optional, secondary)

Priority:

```
CLI > ENV > config.yml
```

---

## 3. Configuration Sections

Recommended structure:

```
general:
data_sources:
universe_filters:
exclusions:
mapping:
features:
scoring:
backtest:
logging:
```

---

## 4. General

```yaml
general:
  run_mode: "standard" # "standard", "fast", "offline", "backtest"
  timezone: "UTC"
  shortlist_size: 100
  lookback_days_1d: 120
  lookback_days_4h: 30
```

---

## 5. Data Sources

```yaml
data_sources:
  mexc:
    enabled: true
    max_retries: 3
    retry_backoff_seconds: 3

  market_cap:
    provider: "cmc"
    api_key_env_var: "CMC_API_KEY"
    max_retries: 3
    bulk_limit: 5000
```

Rate limit configuration should be static per provider.

---

## 6. Universe Filters

```yaml
universe_filters:
  market_cap:
    min_usd: 100000000 # 100M
    max_usd: 3000000000 # 3B
  volume:
    min_quote_volume_24h: 1000000
  history:
    min_history_days_1d: 60
  include_only_usdt_pairs: true
```

---

## 7. Exclusions

```yaml
exclusions:
  exclude_stablecoins: true
  exclude_wrapped_tokens: true
  exclude_leveraged_tokens: true
  exclude_synthetic_derivatives: true

  stablecoin_patterns: ["USD", "USDT", "USDC", "EURT"]
  wrapped_patterns: ["WETH", "WBTC", "st", "stk", "w"]
  leveraged_patterns: ["UP", "DOWN", "BULL", "BEAR", "3L", "3S"]
```

Pattern rules avoid false positives.

---

## 8. Mapping

```yaml
mapping:
  require_high_confidence: false
  overrides_file: "config/mapping_overrides.json"
  collisions_report_file: "reports/mapping_collisions.csv"
  unmapped_behavior: "filter" # or "warn"
```

Mapping stability is crucial for reproducibility.

---

## 9. Features

```yaml
features:
  timeframes:
    - "1d"
    - "4h"

  ema_periods:
    - 20
    - 50

  atr_period: 14

  high_low_lookback_days:
    breakout: 30
    reversal: 60

  volume_sma_period: 7
  volume_spike_threshold: 1.5

  drawdown_lookback_days: 365
```

Feature parameters affect scoring.

---

## 10. Scoring

### 10.1 Breakout

```yaml
scoring:
  breakout:
    enabled: true
    high_lookback_days: 30
    min_volume_spike_factor: 1.5
    max_overextension_ema20_percent: 25
    weights:
      price_break: 0.40
      volume_confirmation: 0.40
      volatility_context: 0.20
```

---

### 10.2 Pullback

```yaml
  pullback:
    enabled: true
    max_pullback_from_high_percent: 25
    min_trend_days: 10
    ema_trend_period_days: 20
    weights:
      trend_quality: 0.40
      pullback_quality: 0.40
      rebound_signal: 0.20
```

---

### 10.3 Reversal

```yaml
  reversal:
    enabled: true
    min_drawdown_from_ath_percent: 40
    max_drawdown_from_ath_percent: 90
    base_lookback_days: 45
    min_base_days_without_new_low: 10
    max_allowed_new_low_percent_vs_base_low: 3
    min_reclaim_above_ema_days: 1
    min_volume_spike_factor: 1.5
    weights:
      base_structure: 0.30
      reclaim_signal: 0.40
      volume_confirmation: 0.30
```

---

## 11. Backtest

```yaml
backtest:
  enabled: true
  forward_return_days: [7, 14, 30]
  max_holding_days: 30
  entry_price: "close"
  exit_price: "close_forward"
  slippage_bps: 10
```

---

## 12. Logging

```yaml
logging:
  level: "INFO"
  file: "logs/scanner.log"
  log_to_file: true
```

---

## 13. Versioning

Configuration changes must increment:

- `config_version`
- `spec_version`

Format:

```yaml
version:
  config: 1.0
  spec: 1.0
```

---

## 14. Anti-Goofs (Important)

Config must **not**:

- contain fuzzy logic
- depend on ML
- rely on sentiment/news
- mix setup type parameters
- implicitly couple scoring modules
- silently change behavior across runs

---

## 15. Extensibility

Config must support additions without breaking v1:

- new scores
- new filters
- new penalties
- new timeframes
- new data sources

Backward compatibility is desirable but not required for v1.

---

## End of `config.md`
