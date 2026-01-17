"""
OHLCV fetch & caching.

Responsibilities:
- For shortlisted assets, fetch OHLCV time series from MEXC:
  - 1d candles (primary structure timeframe)
  - 4h candles (refinement timeframe)
- Handle:
  - time window selection (lookback)
  - rate limiting & retries
  - basic caching (optional, v1 can be simple)
- Provide clean OHLCV data structures to the feature engine.
"""

