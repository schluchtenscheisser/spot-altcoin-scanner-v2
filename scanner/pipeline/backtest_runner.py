"""
Backtest runner.

Responsibilities:
- Consume historical snapshots.
- Compute forward returns for each setup:
  - Breakout
  - Pullback
  - Reversal
- Aggregate evaluation metrics:
  - hit rate
  - median/mean returns
  - tail risk
  - rank vs return behavior
- Output backtest summaries (e.g. JSON / Markdown).

Backtests must be deterministic and snapshot-driven.
"""

