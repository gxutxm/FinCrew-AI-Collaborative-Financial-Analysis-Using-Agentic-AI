"""
ORCHESTRATOR
=============
Connects all three agents to generate a complete financial report.

Flow:
1. User inputs ticker + date range
2. Market Research Agent → sentiment + news
3. Data Analyst Agent → metrics + charts
4. Report Writer Agent → final report
"""

import sys
sys.path.append('data_analyst_agent')
sys.path.append('market_research_agent')
sys.path.append('report_writer')

from agent import DataAnalystAgent
from market_research_agent import analyze_market, to_report_format as market_to_report
from report_writer_agent import generate_full_report
from report_generator import generate_pdf_report


def run_analysis(ticker: str, start_date: str, end_date: str) -> str:
    """
    Run complete financial analysis pipeline.
    
    Parameters:
        ticker: Stock symbol (e.g., 'AAPL')
        start_date: Format 'YYYY-MM-DD'
        end_date: Format 'YYYY-MM-DD'
    
    Returns:
        Complete financial report as string
    """
    print(f"\n{'='*60}")
    print(f"FINCREW ANALYSIS: {ticker}")
    print(f"Period: {start_date} to {end_date}")
    print(f"{'='*60}\n")
    
    # Step 1: Market Research
    print("[1/3] Running Market Research Agent...")
    market_result = analyze_market(ticker, start_date, end_date)
    
    if not market_result['success']:
        print(f"  ⚠ Warning: {market_result['error']}")
        # Use fallback data
        market_data = {
            "sentiment": "Neutral",
            "confidence_score": 0.0,
            "key_risks": ["Unable to fetch news data"],
            "summary": ["Market research unavailable"]
        }
    else:
        market_data = market_to_report(market_result)["market_research"]
        print(f"  ✓ Sentiment: {market_data['sentiment']}")
        print(f"  ✓ Confidence: {market_data['confidence_score']}")
    
    # Step 2: Data Analyst
    print("\n[2/3] Running Data Analyst Agent...")
    analyst = DataAnalystAgent(output_dir="data_analyst_agent/outputs")
    quant_result = analyst.run(ticker, start_date, end_date)
    
    if not quant_result['success']:
        print(f"  ✗ Error: {quant_result.get('errors', 'Unknown error')}")
        return None
    
    quant_data = analyst.to_report_format(quant_result)["quant_analysis"]
    print(f"  ✓ Total Return: {quant_result['metrics']['total_return']*100:.2f}%")
    print(f"  ✓ Volatility: {quant_result['metrics']['volatility_annual']*100:.2f}%")
    print(f"  ✓ Charts saved to: data_analyst_agent/outputs/")
    
    # Step 3: Generate Report
    print("\n[3/3] Generating Report...")
    report = generate_full_report(market_data, quant_data)
    print("  ✓ Report generated!")
    
    return report


if __name__ == "__main__":
    # Get user input
    print("\n" + "="*60)
    print("FINCREW - AI Financial Analysis System")
    print("="*60)
    
    ticker = input("\nEnter stock ticker (e.g., AAPL): ").upper().strip()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()
    
    # Run analysis
    report = run_analysis(ticker, start_date, end_date)
    
    if report:
        print("\n" + "="*60)
        print("FINAL REPORT")
        print("="*60)
        print(report)
        
        # Generate PDF
        print("\nGenerating PDF report...")
        
        # Get the data again for PDF
        market_result = analyze_market(ticker, start_date, end_date)
        if market_result['success']:
            market_data = market_to_report(market_result)["market_research"]
        else:
            market_data = {
                "sentiment": "Neutral",
                "confidence_score": 0.0,
                "key_risks": ["Unable to fetch news data"],
                "summary": ["Market research unavailable"]
            }
        
        analyst = DataAnalystAgent(output_dir="data_analyst_agent/outputs")
        quant_result = analyst.run(ticker, start_date, end_date)
        quant_data = analyst.to_report_format(quant_result)["quant_analysis"]
        
        pdf_path = generate_pdf_report(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            market_data=market_data,
            quant_data=quant_data
        )
        
        print(f"\n✓ PDF Report saved to: {pdf_path}")
        print(f"✓ Charts embedded in report")