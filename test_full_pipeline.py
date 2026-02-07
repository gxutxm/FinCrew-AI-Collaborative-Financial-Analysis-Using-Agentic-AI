"""
Full Pipeline Test
Combines all three agents to generate a report.
"""

import sys
sys.path.append('data_analyst_agent')
sys.path.append('report_writer')

from agent import DataAnalystAgent
from report_writer_agent import generate_full_report


# Step 1: Run Data Analyst Agent (YOUR PART)
print("Running Data Analyst Agent...")
analyst = DataAnalystAgent(output_dir="data_analyst_agent/outputs")
result = analyst.run("AAPL", "2024-01-01", "2024-12-31")
quant_data = analyst.to_report_format(result)["quant_analysis"]
print(f"Quant data ready: {quant_data}\n")


# Step 2: Market Research Data (MOCK - Student 1's part)
# In real use, this comes from market_research_agent
market_data = {
    "sentiment": "Bullish",
    "confidence_score": 0.75,
    "key_risks": ["Interest rate hikes", "China trade tensions"],
    "summary": ["Strong iPhone sales", "Services revenue growing", "AI investments paying off"]
}
print(f"Market data ready: {market_data}\n")


# Step 3: Generate Report (Student 3's part)
print("Generating report...\n")
print("=" * 60)
report = generate_full_report(market_data, quant_data)
print(report)
print("=" * 60)