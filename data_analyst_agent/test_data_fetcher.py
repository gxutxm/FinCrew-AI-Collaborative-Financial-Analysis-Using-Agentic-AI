"""
Test file for data fetcher module.
"""

from data_fetcher import fetch_stock_data


# Test 1: Valid inputs
print("Test 1: Valid inputs")
result = fetch_stock_data("AAPL", "2024-01-01", "2024-12-31")
print(f"Success: {result['success']}")
print(f"Trading days: {result['metadata'].get('trading_days', 'N/A')}")
print(f"Columns: {list(result['data'].columns)}")
print(f"First row:\n{result['data'].head(1)}")

# Test 2: Bad date format
print("\n\nTest 2: Bad date format")
result = fetch_stock_data("AAPL", "01-01-2024", "2024-12-31")
print(f"Success: {result['success']}, Errors: {result['metadata']['errors']}")

# Test 3: Invalid ticker
print("\n\nTest 3: Invalid ticker")
result = fetch_stock_data("XYZFAKE123", "2024-01-01", "2024-12-31")
print(f"Success: {result['success']}, Errors: {result['metadata']['errors']}")