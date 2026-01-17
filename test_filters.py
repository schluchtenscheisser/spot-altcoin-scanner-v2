"""
Test für scanner/pipeline/filters.py
"""

import sys
sys.path.insert(0, '.')

from scanner.pipeline.filters import UniverseFilters

# Test-Config
test_config = {
    'filters': {
        'mcap_min': 100_000_000,  # 100M
        'mcap_max': 3_000_000_000,  # 3B
        'min_volume_24h': 1_000_000,  # 1M
        'exclusion_patterns': ['USDT', 'USDC', 'WBTC', 'UP', 'DOWN']
    }
}

# Test-Daten (simuliert)
test_symbols = [
    # Should PASS all filters
    {
        'symbol': 'BTCUSDT',
        'base': 'BTC',
        'quote_volume_24h': 5_000_000,
        'market_cap': 500_000_000  # 500M (MidCap)
    },
    # Should FAIL - MCAP too high
    {
        'symbol': 'ETHUSDT',
        'base': 'ETH',
        'quote_volume_24h': 10_000_000,
        'market_cap': 5_000_000_000  # 5B (too high)
    },
    # Should FAIL - MCAP too low
    {
        'symbol': 'SMALLUSDT',
        'base': 'SMALL',
        'quote_volume_24h': 2_000_000,
        'market_cap': 50_000_000  # 50M (too low)
    },
    # Should FAIL - Volume too low
    {
        'symbol': 'ILIQUIDUSDT',
        'base': 'ILIQUID',
        'quote_volume_24h': 500_000,  # 500K (too low)
        'market_cap': 200_000_000
    },
    # Should FAIL - Excluded (stablecoin)
    {
        'symbol': 'USDTUSDT',
        'base': 'USDT',
        'quote_volume_24h': 50_000_000,
        'market_cap': 1_000_000_000
    },
    # Should PASS
    {
        'symbol': 'SOLUSDT',
        'base': 'SOL',
        'quote_volume_24h': 8_000_000,
        'market_cap': 1_500_000_000  # 1.5B (MidCap)
    },
    # Should FAIL - No market cap data
    {
        'symbol': 'UNKNOWNUSDT',
        'base': 'UNKNOWN',
        'quote_volume_24h': 3_000_000,
        'market_cap': None
    }
]

print("=" * 80)
print("TEST: UniverseFilters")
print("=" * 80)

# Initialize filters
filters = UniverseFilters(test_config)

print("\n--- INPUT ---")
print(f"Total symbols: {len(test_symbols)}")
for s in test_symbols:
    print(f"  {s['symbol']}: MCAP={s['market_cap']}, VOL={s['quote_volume_24h']}")

print("\n--- RUNNING FILTERS ---")
filtered = filters.apply_all(test_symbols)

print("\n--- OUTPUT ---")
print(f"Filtered symbols: {len(filtered)}")
for s in filtered:
    print(f"  ✓ {s['symbol']}: MCAP={s['market_cap']}, VOL={s['quote_volume_24h']}")

print("\n--- STATISTICS ---")
stats = filters.get_filter_stats(test_symbols)
for key, value in stats.items():
    print(f"  {key}: {value}")

print("\n--- EXPECTED vs ACTUAL ---")
expected_pass = ['BTCUSDT', 'SOLUSDT']
actual_pass = [s['symbol'] for s in filtered]

print(f"Expected: {expected_pass}")
print(f"Actual:   {actual_pass}")

if sorted(expected_pass) == sorted(actual_pass):
    print("\n✅ TEST PASSED!")
else:
    print("\n❌ TEST FAILED!")
    print(f"Missing: {set(expected_pass) - set(actual_pass)}")
    print(f"Extra: {set(actual_pass) - set(expected_pass)}")

print("\n" + "=" * 80)
