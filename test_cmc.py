import os
from scanner.clients.marketcap_client import MarketCapClient

# Check API key
api_key = os.getenv("CMC_API_KEY")
if not api_key:
    print("❌ CMC_API_KEY not set in environment!")
    print("Set it with: export CMC_API_KEY='your-key-here'")
    exit(1)

print(f"✅ API Key found: {api_key[:8]}...")

# Initialize client
client = MarketCapClient()

# Test 1: Get listings
print("\nFetching listings...")
listings = client.get_listings(limit=100)
print(f"✅ Fetched {len(listings)} listings")
print(f"   Top 3: {[l['symbol'] for l in listings[:3]]}")

# Test 2: Build symbol map
print("\nBuilding symbol map...")
symbol_map = client.build_symbol_map(listings)
print(f"✅ Symbol map: {len(symbol_map)} unique symbols")

# Test 3: Get market cap for BTC
btc_mcap = client.get_market_cap_for_symbol("BTC", symbol_map)
print(f"✅ BTC market cap: ${btc_mcap:,.0f}")

print("\n🎉 CMC Client functional!")
