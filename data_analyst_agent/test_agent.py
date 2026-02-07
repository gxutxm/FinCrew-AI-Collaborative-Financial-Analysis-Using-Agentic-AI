"""
Test file for the Data Analyst Agent.
"""

import json
from agent import DataAnalystAgent


# Create the agent
agent = DataAnalystAgent(output_dir="outputs")

# Test 1: Valid stock
print("=" * 60)
print("TEST 1: Valid Stock (AAPL)")
print("=" * 60)
result = agent.run("AAPL", "2024-01-01", "2024-12-31")
print(f"Success: {result['success']}")
print(f"\nFull output:")
print(json.dumps(result, indent=2))

# Test 2: Invalid ticker
print("\n" + "=" * 60)
print("TEST 2: Invalid Ticker")
print("=" * 60)
result = agent.run("XYZFAKE123", "2024-01-01", "2024-12-31")
print(f"Success: {result['success']}")
print(f"Errors: {result.get('errors', [])}")

# Test 3: Report format output
print("\n" + "=" * 60)
print("TEST 3: Report Writer Format")
print("=" * 60)
result = agent.run("AAPL", "2024-01-01", "2024-12-31")
report_format = agent.to_report_format(result)
print(json.dumps(report_format, indent=2))