import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from Stock import Stock

def get_color(window_int:int) -> str:
    match window_int:
        case 50 : return 'blue'
        case 100: return 'orange'
        case 150: return 'green'
        case 200: return 'red'

def get_width_linestyle(period: str) -> tuple[int, str]:
    match period:
        case 'daily': return 1, ':'
        case 'weekly': return 1, '-.'
        case 'monthly': return 1, '-'
    return 1, '-'  # default

def get_interval(period : str) -> str:
    match period:
        case 'daily': return '1d' 
        case 'weekly': return '1wk' 
        case 'monthly': return '1mo'
    
def get_interpolated_MA(sma : pd.DataFrame, source_df : pd.DataFrame) -> pd.DataFrame:
    sma = sma.dropna()
    expanded_series = pd.Series(index=source_df.index, dtype='float64')
    expanded_series.update(sma)
    interpolated_series = expanded_series.interpolate(method='time')
    return interpolated_series.ffill().bfill()

def plot_with_levels(stock: Stock, buy_signal: dict):
    # Download historical data
    df = stock.daily_hist

    date_mask = pd.Timestamp.today(tz='America/New_York') - pd.DateOffset(years=1)
    df_masked = df[df.index >= date_mask]

    # Flatten MultiIndex columns as sometimes, yfinance returns a DataFrame where the columns are a MultiIndex (e.g., ('Close', ''), ('Volume', '')). 
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0) # only select the first level
    
    # Ensure correct format
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    df = df[required_cols].copy()
    df = df.dropna(subset=required_cols)  # Drop rows with NaNs

    # Convert to correct types just to be safe
    df[required_cols] = df[required_cols].astype(float)
    df.index.name = 'Date'

    mpf_supports = []

    # Support lines
    if 'support_level' in buy_signal:
        for level in buy_signal['support_level']:
            mpf_supports.append(mpf.make_addplot([level]*len(df_masked), color='gray', width=1, linestyle='--'))

    mpf_moving_averages = []

    if 'moving_average' in buy_signal:
        for ma_key, _ in buy_signal['moving_average'].items():
            period, window_str, _ = ma_key.split('_')
            interval = get_interval(period)
            window = int(window_str)
            sma = stock.stock.history(period='10y', interval=interval).rolling(window=window).mean()['Close']
            interpolated_series = get_interpolated_MA(sma, df_masked)        
            color = get_color(int(window_str))
            width,linestyle = get_width_linestyle(period)      
            mpf_moving_averages.append(mpf.make_addplot(interpolated_series, color=color, width=width, linestyle=linestyle))
    # Plot and return figure and axes
    fig, axes = mpf.plot(
        df_masked,
        type='candle',
        style='yahoo',
        title=f"{buy_signal['ticker']} Candlestick Chart",
        ylabel='Price ($)',
        addplot=mpf_supports + mpf_moving_averages,
        figratio=(21, 9),
        figscale=1.2,
        returnfig=True
    )

    # Access main price axis (first panel)
    ax = axes[0]

    # === Gridlines ===
    ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.minorticks_on()
    ax.tick_params(axis='x', which='minor', length=4)
    ax.tick_params(axis='x', which='major', length=8)
    ax.grid(which='minor', linestyle=':', linewidth=0.3, alpha=0.5)

    # === Legend Setup ===
    legend_handles = []

    # Support levels
    if 'support_level' in buy_signal:
        support_line = Line2D([], [], color='gray', linestyle='--', label='Support/Resistance Levels')
        legend_handles.append(support_line)

    # Moving averages
    if 'moving_average' in buy_signal:
        for ma_key, value in buy_signal['moving_average'].items():
            period, window_str, _ = ma_key.split('_')
            color = get_color(int(window_str))
            width,linestyle = get_width_linestyle(period)
            label = ma_key.replace('_', ' ').title()
            ma_line = Line2D([], [], color=color, linestyle=linestyle, label=label)
            legend_handles.append(ma_line)

    # Add legend to the top-left of the chart
    ax.legend(handles=legend_handles, loc='upper left', fontsize=8, frameon=False)

    plt.show()