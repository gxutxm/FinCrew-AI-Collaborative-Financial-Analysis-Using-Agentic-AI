"""
Test file for visualizer module.
"""

from data_fetcher import fetch_stock_data
from visualizer import plot_price_with_ma
from visualizer import plot_price_with_ma, plot_rsi
from visualizer import plot_price_with_ma, plot_rsi, plot_drawdown
from visualizer import plot_price_with_ma, plot_rsi, plot_drawdown, generate_all_charts


# Fetch data once for all tests
print("Fetching AAPL data...")
result = fetch_stock_data("AAPL", "2024-01-01", "2024-12-31")
df = result['data']
print(f"Got {len(df)} trading days\n")


# Test: Price Chart
print("--- Price Chart ---")
path = plot_price_with_ma(df, "AAPL", output_dir="outputs")
print(f"Saved to: {path}")

# Test: RSI Chart
print("\n--- RSI Chart ---")
path = plot_rsi(df, "AAPL", output_dir="outputs")
print(f"Saved to: {path}")

# Test: Drawdown Chart
print("\n--- Drawdown Chart ---")
path = plot_drawdown(df, "AAPL", output_dir="outputs")
print(f"Saved to: {path}")

# Test: All Charts
print("\n--- ALL CHARTS ---")
charts = generate_all_charts(df, "AAPL", output_dir="outputs")
print("Generated charts:")
for name, path in charts.items():
    print(f"  {name}: {path}")