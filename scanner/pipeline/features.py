"""
Feature engine.

Responsibilities:
- Transform raw OHLCV data into structured features:
  - returns (1d, 3d, 7d)
  - EMA20, EMA50
  - ATR% (volatility)
  - 20–30d highs/lows
  - drawdown from ATH
  - volume SMA & volume spikes
  - basic HH/HL structure
- Output deterministic feature dictionaries per asset and timeframe,
  as specified in docs/features.md and docs/data_model.md.
"""

