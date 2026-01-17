"""
Cheap-pass shortlist selection.

Responsibilities:
- Take the filtered universe and select a shortlist of assets
  for the expensive OHLCV + feature + scoring pass.
- Use cheap information only, e.g.:
  - 24h quote volume
  - 24h price change
- Ensure shortlist size matches config (e.g. 80–120 assets).
"""

