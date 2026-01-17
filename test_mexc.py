from scanner.clients.mexc_client import MEXCClient
import json

client = MEXCClient()

# DEBUG: Zeige API-Struktur
print("=" * 50)
print("DEBUG: MEXC API Structure")
print("=" * 50)

info = client.get_exchange_info()
first_symbol = info['symbols'][0]
print(json.dumps(first_symbol, indent=2))

print("\n" + "=" * 50)
print("Checking what fields exist...")
print("=" * 50)
print(f"Keys in symbol: {list(first_symbol.keys())}")
