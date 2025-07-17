from Stock import Stock
import pandas as pd

def _calculate_latest_sma(df: pd.DataFrame, window: int) -> float | None:
    if df.empty:
        return None
    # Calculate rolling mean and get the last available value
    return df['Close'].rolling(window=window).mean().iloc[-1]

def get_moving_averages(stock: Stock) -> dict[str, float]:
    print(f"Fetching moving averages for {stock.ticker}...")
    all_sma = {}

    # Define intervals and their corresponding dataframes and windows
    intervals_config = {
        'daily': {'df': stock.daily_hist, 'windows': [150, 200],'weight': 1},
        'weekly': {'df': stock.weekly_hist, 'windows': [50, 100, 150, 200], 'weight': 1.5},
        'monthly': {'df': stock.monthly_hist, 'windows': [50],'weight': 1.5}
    }

    for interval_name, config in intervals_config.items():
        df = config['df']
        for window in config['windows']:
            sma_value = _calculate_latest_sma(df, window)
            if sma_value is not None:
                all_sma[f'{interval_name}_{window}_sma'] = [sma_value,config['weight']]
    
    return all_sma