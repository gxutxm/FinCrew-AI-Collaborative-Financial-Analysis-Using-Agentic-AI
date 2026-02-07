from data_fetcher import fetch_stock_data
from metrics import compute_all_metrics
from visualizer import generate_all_charts

class DataAnalystAgent:
    """
    Main agent class that orchestrates data fetching, metrics, and charts.
    """
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize the agent.
        
        Parameters:
            output_dir: Where to save chart images
        """
        self.output_dir = output_dir
    
    def run(self, ticker: str, start_date: str, end_date: str) -> dict:
        """
        Run the full analysis pipeline.
        
        Parameters:
            ticker: Stock symbol (e.g., 'AAPL')
            start_date: Format 'YYYY-MM-DD'
            end_date: Format 'YYYY-MM-DD'
            
        Returns:
            dict with metrics, chart paths, and status
        """
        # Step 1: Fetch data
        fetch_result = fetch_stock_data(ticker, start_date, end_date)
        
        if not fetch_result['success']:
            return {
                'ticker': ticker.upper(),
                'success': False,
                'errors': fetch_result['metadata']['errors']
            }
        
        df = fetch_result['data']
        
        # Step 2: Calculate metrics
        metrics = compute_all_metrics(df, ticker)
        
        # Step 3: Generate charts
        charts = generate_all_charts(df, ticker, self.output_dir)
        
        # Step 4: Return combined result
        return {
            'ticker': ticker.upper(),
            'period': metrics['period'],
            'metrics': metrics['metrics'],
            'charts': charts,
            'success': True
        }
    
    def to_report_format(self, result: dict) -> dict:
        """
        Convert output to Report Writer's expected schema.
        """
        if not result['success']:
            return {"quant_analysis": {}, "error": result.get('errors', [])}
        
        # Handle NaN values
        import math
        rsi = result["metrics"]["rsi_current"]
        rsi_int = 50 if math.isnan(rsi) else int(rsi)
        
        return {
            "quant_analysis": {
                "volatility": result["metrics"]["volatility_annual"],
                "avg_return": result["metrics"]["avg_daily_return"],
                "RSI": rsi_int,
                "max_drawdown": result["metrics"]["max_drawdown"]
            }
        }