"""
Test file for metrics module.
"""

from data_fetcher import fetch_stock_data
from metrics import calculate_daily_returns
from metrics import calculate_daily_returns, calculate_volatility
from metrics import calculate_daily_returns, calculate_volatility, calculate_moving_averages
from metrics import calculate_daily_returns, calculate_volatility, calculate_moving_averages, calculate_rsi
from metrics import calculate_daily_returns, calculate_volatility, calculate_moving_averages, calculate_rsi, calculate_max_drawdown
from metrics import calculate_daily_returns, calculate_volatility, calculate_moving_averages, calculate_rsi, calculate_max_drawdown, calculate_total_return
from metrics import calculate_daily_returns, calculate_volatility, calculate_moving_averages, calculate_rsi, calculate_max_drawdown, calculate_total_return, compute_all_metrics


# Fetch data once for all tests
print("Fetching AAPL data...")
result = fetch_stock_data("AAPL", "2024-01-01", "2024-12-31")
df = result['data']
print(f"Got {len(df)} trading days\n")


# Test: Daily Returns
print("--- Daily Returns ---")
returns = calculate_daily_returns(df)
print(f"First 5 returns:\n{returns.head()}")
print(f"\nAverage daily return: {returns.mean():.4f}")
print(f"Best day: {returns.max():.4f} ({returns.max()*100:.2f}%)")
print(f"Worst day: {returns.min():.4f} ({returns.min()*100:.2f}%)")

# Test: Volatility
print("\n--- Volatility ---")
vol = calculate_volatility(df)
print(f"Annual volatility: {vol:.4f} ({vol*100:.2f}%)")

# Test: Moving Averages
print("\n--- Moving Averages ---")
ma = calculate_moving_averages(df)
print(f"Columns: {list(ma.columns)}")
print(f"\nLast 5 rows:")
print(ma.tail())

# Test: RSI
print("\n--- RSI ---")
rsi = calculate_rsi(df)
print(f"Current RSI: {rsi.iloc[-1]:.2f}")
print(f"Max RSI: {rsi.max():.2f}")
print(f"Min RSI: {rsi.min():.2f}")

if rsi.iloc[-1] > 70:
    print("Signal: Overbought")
elif rsi.iloc[-1] < 30:
    print("Signal: Oversold")
else:
    print("Signal: Neutral")

# Test: Max Drawdown
print("\n--- Max Drawdown ---")
dd = calculate_max_drawdown(df)
print(f"Max Drawdown: {dd['max_drawdown']:.4f} ({dd['max_drawdown']*100:.2f}%)")
print(f"Peak date: {dd['peak_date']}")
print(f"Trough date: {dd['trough_date']}")

# Test: Total Return
print("\n--- Total Return ---")
total_ret = calculate_total_return(df)
print(f"Total Return: {total_ret:.4f} ({total_ret*100:.2f}%)")

# Test: All Metrics Combined
print("\n--- ALL METRICS (JSON Output) ---")
import json
all_metrics = compute_all_metrics(df, "AAPL")
print(json.dumps(all_metrics, indent=2))

