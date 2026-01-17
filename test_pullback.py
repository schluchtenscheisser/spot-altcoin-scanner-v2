"""
Test für scanner/pipeline/scoring/pullback.py
"""

import sys
sys.path.insert(0, '.')

from scanner.pipeline.scoring.pullback import PullbackScorer, score_pullbacks

print("=" * 80)
print("TEST: Pullback Scorer")
print("=" * 80)

# Test config
test_config = {
    'scoring': {
        'pullback': {
            'min_trend_strength': 5,
            'ideal_pullback_depth': 5,
            'max_pullback_depth': 15,
            'min_rebound': 3,
            'min_volume_spike': 1.3
        }
    }
}

# Mock features
mock_features = {
    'PERFECTPB': {  # Perfect pullback
        '1d': {
            'close': 1.0,
            'dist_ema20_pct': 1.0,  # Near EMA20 (support)
            'dist_ema50_pct': 10.0,  # Strong uptrend
            'hh_20': True,  # Higher highs
            'r_3': 8.0,  # Good rebound
            'volume_spike': 2.2  # Volume on rebound
        },
        '4h': {
            'r_3': 4.0,
            'volume_spike': 2.5
        }
    },
    'NOPB': {  # No pullback (still extended)
        '1d': {
            'close': 1.0,
            'dist_ema20_pct': 15.0,  # Far above EMA20
            'dist_ema50_pct': 20.0,  # Extended
            'hh_20': True,
            'r_3': 1.0,  # No rebound needed
            'volume_spike': 1.0
        },
        '4h': {
            'r_3': 0.5,
            'volume_spike': 0.9
        }
    },
    'BROKENPB': {  # Broken trend
        '1d': {
            'close': 1.0,
            'dist_ema20_pct': -5.0,  # Below EMA20
            'dist_ema50_pct': -3.0,  # Below EMA50 (broken!)
            'hh_20': False,
            'r_3': 2.0,
            'volume_spike': 1.5
        },
        '4h': {
            'r_3': 1.0,
            'volume_spike': 1.4
        }
    }
}

mock_volumes = {
    'PERFECTPB': 2_000_000,
    'NOPB': 1_500_000,
    'BROKENPB': 800_000
}

print("\n--- Initializing Pullback Scorer ---")
scorer = PullbackScorer(test_config)
print("✓ Scorer ready")

print("\n--- Scoring Individual Symbols ---")
for symbol, features in mock_features.items():
    volume = mock_volumes.get(symbol, 0)
    result = scorer.score(symbol, features, volume)
    
    print(f"\n{symbol}:")
    print(f"  Score: {result['score']:.2f}")
    print(f"  Components:")
    for comp, val in result['components'].items():
        print(f"    {comp}: {val:.2f}")
    
    if result['penalties']:
        print(f"  Penalties:")
        for pen, factor in result['penalties'].items():
            print(f"    {pen}: {factor:.2f}x")
    
    if result['flags']:
        print(f"  Flags: {', '.join(result['flags'])}")
    
    print(f"  Reasons:")
    for reason in result['reasons']:
        print(f"    - {reason}")

print("\n--- Batch Scoring & Ranking ---")
ranked = score_pullbacks(mock_features, mock_volumes, test_config)

print(f"\nRanked List:")
for i, entry in enumerate(ranked, 1):
    print(f"{i}. {entry['symbol']}: {entry['score']:.2f}")

# Validation
print("\n--- Validation ---")
success = True

# PERFECTPB should rank first
if ranked[0]['symbol'] != 'PERFECTPB':
    print("❌ PERFECTPB should rank first")
    success = False
else:
    print("✓ PERFECTPB ranks first")

# BROKENPB should be flagged
broken = next(r for r in ranked if r['symbol'] == 'BROKENPB')
if 'broken_trend' not in broken['flags']:
    print("❌ BROKENPB should be flagged as broken_trend")
    success = False
else:
    print("✓ BROKENPB flagged as broken_trend")

# NOPB should have lower score than PERFECTPB
nopb = next(r for r in ranked if r['symbol'] == 'NOPB')
if nopb['score'] >= ranked[0]['score']:
    print("❌ NOPB should score lower than PERFECTPB")
    success = False
else:
    print(f"✓ NOPB scores lower ({nopb['score']:.2f})")

if success:
    print("\n✅ TEST PASSED!")
else:
    print("\n❌ TEST FAILED!")

print("\n" + "=" * 80)
