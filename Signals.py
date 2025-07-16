from Stock import Stock
import mplfinance as mpf
import yfinance as yf
import pandas as pd
def check_buy_signal(stock: Stock, supports: list[float], moving_average: dict)-> dict | None:
    current_price = [stock.current_high, stock.current_low, stock.current_open, stock.current_close]
    signal = {
        'ticker': stock.ticker,
        'score': 0,
        'current_price': current_price[-1]
    }

    for support in supports:
        for price in current_price:
            if abs(price - support) / support * 100 <= 5:
                signal['score'] += 1                
                if 'support_level' not in signal:
                    signal['support_level'] = []
                signal['support_level'].append(support)
                break
    for ma_key, (ma_value, weight) in moving_average.items():
        for price in current_price:
            if abs(price - ma_value) / ma_value * 100 <= 5:
                signal['score'] += weight
                if 'moving_average' not in signal:
                    signal['moving_average'] = {}
                signal['moving_average'][ma_key] = ma_value
                break
    if signal['score'] >= 1.5:
        return signal    
    return None

def plot_with_levels(stock: Stock, buy_signal: dict):
    mpf_supports = []
    mpf_moving_averages = []

    df = yf.download(stock.ticker, period="2y", interval="1d")
    end_date = df.index.max()
    start_date = end_date - pd.DateOffset(years=1)

    # Flatten MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    df = df[required_cols].copy()
    df = df.dropna(subset=required_cols)
    df.index.name = 'Date'

    # Determine if it's a 7-day instrument (e.g., BTC)
    df_days_per_week = df.index.to_series().diff().dt.days
    trades_every_day = df_days_per_week.value_counts().get(1, 0) / len(df_days_per_week) > 0.9

    def get_days(period, window):
        if trades_every_day:
            if period == "weekly":
                return 7 * window
            elif period == "monthly":
                return 30 * window
        else:
            if period == "weekly":
                return 5 * window
            elif period == "monthly":
                return 21 * window
        return window  # for 'daily'

    # Support lines
    if 'support_level' in buy_signal:
        for level in buy_signal['support_level']:
            mpf_supports.append(mpf.make_addplot([level]*len(df), color='gray', width=1, linestyle='--'))

    # Moving averages
    if 'moving_average' in buy_signal:
        for ma_key, _ in buy_signal['moving_average'].items():
            period, window_str, _ = ma_key.split('_')
            window = int(window_str)
            days = get_days(period, window)
            sma = df['Close'].rolling(window=days).mean()
            mpf_moving_averages.append(mpf.make_addplot(sma, color='red', width=1, linestyle='-'))

    # Plot
    mpf.plot(
        df,
        type='candle',
        style='yahoo',
        title=f"{stock.ticker} Candlestick Chart",
        ylabel='Price ($)',
        addplot=mpf_supports + mpf_moving_averages,
        figratio=(18, 10),
        figscale=1.2,
        xlim=(start_date, end_date)  # 👈 this limits visible x-axis to 1 year
    )


                  

    

    # # Download historical data
    # ticker = stock_info['ticker']
    # df = yf.download(ticker, period="6mo", interval="1d")

    # # Flatten MultiIndex columns
    # if isinstance(df.columns, pd.MultiIndex):
    #     df.columns = df.columns.get_level_values(0)

    # # Ensure correct format
    # required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    # df = df[required_cols].copy()
    # df = df.dropna(subset=required_cols)  # Drop rows with NaNs

    # # Convert to correct types just to be safe
    # df[required_cols] = df[required_cols].astype(float)
    # df.index.name = 'Date'

    # # Build signal lines
    # support_levels = stock_info['support_level']
    # moving_avg_200 = stock_info['moving_average']['daily_200_sma']
    # add_plot = []

    # for level in support_levels:
    #     add_plot.append(mpf.make_addplot([level]*len(df), color='green', width=0.8, linestyle='--'))

    # add_plot.append(mpf.make_addplot([moving_avg_200]*len(df), color='orange', width=1, linestyle='-'))

    # # Plot the candlestick chart
    # mpf.plot(
    #     df,
    #     type='candle',
    #     style='yahoo',
    #     title=f"{ticker} Candlestick Chart",
    #     ylabel='Price ($)',
    #     # volume=True,
    #     addplot=add_plot,
    #     figratio=(18,10),
    #     figscale=1.2
    # )