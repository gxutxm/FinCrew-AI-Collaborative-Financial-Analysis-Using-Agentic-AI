"""
METRICS CALCULATOR MODULE

Layer 2 of the Data Analyst Agent

Takes stock price data and computes financial metrics.
"""

import pandas as pd
import numpy as np

def calculate_daily_returns(df: pd.DataFrame) -> pd.Series:
    """
    Calculate daily percentage returns.
    
    Parameters:
        df: DataFrame with 'close' column
        
    Returns:
        Series of daily returns (as decimals, e.g., 0.02 = 2%)
    """
    returns = df['close'].pct_change()
    return returns

def calculate_volatility(df: pd.DataFrame, annualize: bool = True) -> float:
    """
    Calculate stock volatility (standard deviation of returns).
    
    Parameters:
        df: DataFrame with 'close' column
        annualize: If True, multiply by sqrt(252) for annual volatility
        
    Returns:
        Volatility as a decimal (e.g., 0.25 = 25%)
    """
    returns = calculate_daily_returns(df)
    daily_vol = returns.std()
    
    if annualize:
        # 252 trading days in a year
        return daily_vol * np.sqrt(252)
    return daily_vol

def calculate_moving_averages(df: pd.DataFrame, windows: list = [20, 50]) -> pd.DataFrame:
    """
    Calculate Simple Moving Averages (SMA) and Exponential Moving Averages (EMA).
    
    Parameters:
        df: DataFrame with 'close' column
        windows: List of window sizes (e.g., [20, 50] for 20-day and 50-day)
        
    Returns:
        DataFrame with SMA and EMA columns
    """
    result = pd.DataFrame(index=df.index)
    
    for window in windows:
        result[f'sma_{window}'] = df['close'].rolling(window=window).mean()
        result[f'ema_{window}'] = df['close'].ewm(span=window, adjust=False).mean()
    
    return result

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    
    Parameters:
        df: DataFrame with 'close' column
        period: Lookback period (default 14 days)
        
    Returns:
        Series with RSI values (0-100)
    """
    # Get price changes
    delta = df['close'].diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = (-delta).where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_max_drawdown(df: pd.DataFrame) -> dict:
    """
    Calculate maximum drawdown (worst peak-to-trough decline).
    
    Parameters:
        df: DataFrame with 'close' column
        
    Returns:
        dict with max_drawdown, peak_date, trough_date
    """
    prices = df['close']
    
    # Running maximum (highest price seen so far)
    running_max = prices.cummax()
    
    # Drawdown at each point (current price vs peak)
    drawdown = (prices - running_max) / running_max
    
    # Find the worst drawdown
    max_drawdown = drawdown.min()
    trough_date = drawdown.idxmin()
    
    # Find the peak before that trough
    peak_date = prices[:trough_date].idxmax()
    
    return {
        'max_drawdown': max_drawdown,
        'peak_date': peak_date.strftime('%Y-%m-%d'),
        'trough_date': trough_date.strftime('%Y-%m-%d')
    }

def calculate_total_return(df: pd.DataFrame) -> float:
    """
    Calculate total return over the period.
    
    Parameters:
        df: DataFrame with 'close' column
        
    Returns:
        Total return as decimal (e.g., 0.35 = 35%)
    """
    start_price = df['close'].iloc[0]
    end_price = df['close'].iloc[-1]
    
    return (end_price - start_price) / start_price


def compute_all_metrics(df: pd.DataFrame, ticker: str) -> dict:
    """
    Compute all financial metrics for a stock.
    
    This is the MAIN function that other agents will call.
    
    Parameters:
        df: DataFrame with OHLCV data
        ticker: Stock symbol (for labeling)
        
    Returns:
        dict with all metrics in structured format
    """
    drawdown = calculate_max_drawdown(df)
    rsi = calculate_rsi(df)
    
    return {
        'ticker': ticker.upper(),
        'period': {
            'start': df.index.min().strftime('%Y-%m-%d'),
            'end': df.index.max().strftime('%Y-%m-%d'),
            'trading_days': len(df)
        },
        'metrics': {
            'total_return': round(calculate_total_return(df), 4),
            'volatility_annual': round(calculate_volatility(df), 4),
            'max_drawdown': round(drawdown['max_drawdown'], 4),
            'drawdown_peak_date': drawdown['peak_date'],
            'drawdown_trough_date': drawdown['trough_date'],
            'rsi_current': round(rsi.iloc[-1], 2),
            'avg_daily_return': round(calculate_daily_returns(df).mean(), 6)
        }
    }