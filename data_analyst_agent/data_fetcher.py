import yfinance as yf
import pandas as pd
from datetime import datetime


def validate_inputs(ticker: str, start_date: str, end_date: str) -> str:
    """
    Check if inputs are valid.
    
    Returns:
        Empty string if valid, error message if invalid.
    """
    
    # Check ticker
    if not ticker or not isinstance(ticker, str):
        return "Ticker must be a non-empty string"
    
    if len(ticker) > 10:
        return f"Ticker '{ticker}' seems too long"
    
    # Check date formats
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return f"start_date '{start_date}' is not in YYYY-MM-DD format"
    
    try:
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return f"end_date '{end_date}' is not in YYYY-MM-DD format"
    
    # Check date logic
    if start >= end:
        return "start_date must be before end_date"
    
    # All checks passed
    return ""

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw data from Yahoo Finance.
    
    - Flattens MultiIndex columns
    - Converts column names to lowercase
    - Removes rows with missing data
    """
    df = df.copy()
    
    # Flatten MultiIndex columns (e.g., ('Close', 'AAPL') → 'Close')
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Convert to lowercase
    df.columns = [col.lower() for col in df.columns]
    
    # Remove any rows with missing values
    df = df.dropna()
    
    # Sort by date
    df = df.sort_index()
    
    return df


def fetch_stock_data(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Fetch stock data from Yahoo Finance.
    
    Parameters:
    -----------
    ticker : str
        Stock symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')
    start_date : str
        Format: 'YYYY-MM-DD'
    end_date : str
        Format: 'YYYY-MM-DD'
    
    Returns:
    --------
    dict with keys:
        - 'data': pandas DataFrame with OHLCV data
        - 'metadata': dict with fetch info
        - 'success': bool
    """
    
    metadata = {
        'ticker': ticker.upper(),
        'requested_start': start_date,
        'requested_end': end_date,
        'fetch_time': datetime.now().isoformat(),
        'errors': []
    }
    
    # Step 2: Validate inputs
    validation_error = validate_inputs(ticker, start_date, end_date)
    if validation_error:
        metadata['errors'].append(validation_error)
        return {
            'data': pd.DataFrame(),
            'metadata': metadata,
            'success': False
        }
    
    # Step 3: Fetch data from Yahoo Finance
    try:
        df = yf.download(
            tickers=ticker.upper(),
            start=start_date,
            end=end_date,
            progress=False
        )

        df = clean_dataframe(df)
        
        # Check if we got any data
        if df.empty:
            metadata['errors'].append(f"No data found for {ticker}")
            return {
                'data': pd.DataFrame(),
                'metadata': metadata,
                'success': False
            }
            
    except Exception as e:
        metadata['errors'].append(f"Fetch failed: {str(e)}")
        return {
            'data': pd.DataFrame(),
            'metadata': metadata,
            'success': False
        }
    
    # Step 4: Add metadata and return
    metadata['actual_start'] = df.index.min().strftime('%Y-%m-%d')
    metadata['actual_end'] = df.index.max().strftime('%Y-%m-%d')
    metadata['trading_days'] = len(df)
    
    return {
        'data': df,
        'metadata': metadata,
        'success': True
    }

if __name__ == "__main__":
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