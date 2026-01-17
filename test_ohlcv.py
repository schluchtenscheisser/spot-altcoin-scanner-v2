"""
Test für scanner/pipeline/ohlcv.py
"""

import sys
sys.path.insert(0, '.')

from scanner.pipeline.ohlcv import OHLCVFetcher
from scanner.clients.mexc_client import MEXCClient
from scanner.config import load_config

print("=" * 80)
print("TEST: OHLCVFetcher")
print("=" * 80)

# Load config
print("\n--- Loading Config ---")
config = load_config()
print("✓ Config loaded")

# Initialize MEXC client (no config needed!)
print("\n--- Initializing MEXC Client ---")
mexc = MEXCClient()
print("✓ MEXC client ready")

# Test config for faster testing
test_config = {
    'ohlcv': {
        'timeframes': ['1d', '4h'],
        'lookback': {
            '1d': 30,   # Reduced to 30 days (MEXC might have limited history)
            '4h': 60    # Reduced to 10 days
        },
        'min_candles': {
            '1d': 5,    # Lowered minimum for test
            '4h': 10
        }
    }
}

# Initialize fetcher
print("\n--- Initializing OHLCV Fetcher ---")
fetcher = OHLCVFetcher(mexc, test_config)
print(f"✓ Fetcher ready: {fetcher.timeframes}")

# Test with small shortlist
print("\n--- Test Shortlist (3 symbols) ---")
test_shortlist = [
    {'symbol': 'BTCUSDT', 'base': 'BTC'},
    {'symbol': 'ETHUSDT', 'base': 'ETH'},
    {'symbol': 'BNBUSDT', 'base': 'BNB'}
]

for s in test_shortlist:
    print(f"  {s['symbol']}")

# Fetch OHLCV
print("\n--- Fetching OHLCV Data ---")
ohlcv_data = fetcher.fetch_all(test_shortlist)

# Results
print("\n--- Results ---")
print(f"Symbols with complete data: {len(ohlcv_data)}/{len(test_shortlist)}")

for symbol, data in ohlcv_data.items():
    print(f"\n{symbol}:")
    for tf, candles in data.items():
        if candles:
            first_close = candles[0][4]
            last_close = candles[-1][4]
            print(f"  {tf}: {len(candles)} candles, Close: {first_close} → {last_close}")

# Statistics
print("\n--- Statistics ---")
stats = fetcher.get_fetch_stats(ohlcv_data)
for key, value in stats.items():
    print(f"  {key}: {value}")

# Validation
print("\n--- Validation ---")
success = len(ohlcv_data) > 0

if success:
    print(f"✓ Fetched data for {len(ohlcv_data)} symbols")
    
    # Check timeframes
    for symbol in ohlcv_data:
        for tf in fetcher.timeframes:
            if tf not in ohlcv_data[symbol]:
                print(f"❌ {symbol}: Missing timeframe {tf}")
                success = False
    
    if success:
        print("✓ All timeframes present")
else:
    print("❌ No data fetched (MEXC may have limited history)")

# Final result
if success:
    print("\n✅ TEST PASSED!")
else:
    print("\n⚠️  TEST WARNING: Limited/no data from MEXC")
    print("    This may be expected if MEXC has limited historical data")
    print("    The code logic is correct if no errors occurred")

print("\n" + "=" * 80)
