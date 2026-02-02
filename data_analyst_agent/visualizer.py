import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_price_with_ma(df: pd.DataFrame, ticker: str, output_dir: str = "outputs") -> str:
    """
    Create price chart with moving averages.
    
    Parameters:
        df: DataFrame with 'close' column
        ticker: Stock symbol (for title)
        output_dir: Where to save the PNG
        
    Returns:
        Path to saved image
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate moving averages
    sma_20 = df['close'].rolling(window=20).mean()
    sma_50 = df['close'].rolling(window=50).mean()
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    plt.plot(df.index, df['close'], label='Price', color='blue', linewidth=1)
    plt.plot(df.index, sma_20, label='SMA 20', color='orange', linewidth=1)
    plt.plot(df.index, sma_50, label='SMA 50', color='red', linewidth=1)
    
    plt.title(f'{ticker} - Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the figure
    filepath = os.path.join(output_dir, f'{ticker}_price.png')
    plt.savefig(filepath, dpi=150)
    plt.close()
    
    return filepath


def plot_rsi(df: pd.DataFrame, ticker: str, period: int = 14, output_dir: str = "outputs") -> str:
    """
    Create RSI chart with overbought/oversold bands.
    
    Parameters:
        df: DataFrame with 'close' column
        ticker: Stock symbol
        period: RSI lookback period (default 14)
        output_dir: Where to save the PNG
        
    Returns:
        Path to saved image
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate RSI
    delta = df['close'].diff()
    gains = delta.where(delta > 0, 0)
    losses = (-delta).where(delta < 0, 0)
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    
    # Create the plot
    plt.figure(figsize=(12, 4))
    
    plt.plot(df.index, rsi, label='RSI', color='purple', linewidth=1)
    
    # Overbought/Oversold lines
    plt.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(y=30, color='green', linestyle='--', label='Oversold (30)')
    
    plt.title(f'{ticker} - RSI ({period}-day)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save
    filepath = os.path.join(output_dir, f'{ticker}_rsi.png')
    plt.savefig(filepath, dpi=150)
    plt.close()
    
    return filepath


def plot_drawdown(df: pd.DataFrame, ticker: str, output_dir: str = "outputs") -> str:
    """
    Create drawdown chart showing peak-to-trough declines.
    
    Parameters:
        df: DataFrame with 'close' column
        ticker: Stock symbol
        output_dir: Where to save the PNG
        
    Returns:
        Path to saved image
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate drawdown
    prices = df['close']
    running_max = prices.cummax()
    drawdown = (prices - running_max) / running_max * 100  # As percentage
    
    # Create the plot
    plt.figure(figsize=(12, 4))
    
    plt.fill_between(df.index, drawdown, 0, color='red', alpha=0.3)
    plt.plot(df.index, drawdown, color='red', linewidth=1)
    
    plt.title(f'{ticker} - Drawdown')
    plt.xlabel('Date')
    plt.ylabel('Drawdown (%)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save
    filepath = os.path.join(output_dir, f'{ticker}_drawdown.png')
    plt.savefig(filepath, dpi=150)
    plt.close()
    
    return filepath


def generate_all_charts(df: pd.DataFrame, ticker: str, output_dir: str = "outputs") -> dict:
    """
    Generate all charts for a stock.
    
    This is the MAIN function that other agents will call.
    
    Parameters:
        df: DataFrame with OHLCV data
        ticker: Stock symbol
        output_dir: Where to save the PNGs
        
    Returns:
        dict with paths to all generated charts
    """
    charts = {
        'price': plot_price_with_ma(df, ticker, output_dir),
        'rsi': plot_rsi(df, ticker, output_dir=output_dir),
        'drawdown': plot_drawdown(df, ticker, output_dir)
    }
    
    return charts