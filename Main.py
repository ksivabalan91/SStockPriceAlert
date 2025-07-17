from TelegramMsg import save_and_send_plot
from Stock import Stock
from Supports import get_supports
from MovAvg import get_moving_averages
from Signals import check_buy_signal
from Plot import plot_with_levels, generate_captions


tickers = ['PLTR','NVDA','VOO','AMD','AAPL','AMZN','GOOG','MSFT','BTC-USD','ETH-USD']
# tickers = ['NVDA']

for ticker in tickers:
    # Initialize Stock object
    stock = Stock(ticker)
    
    # Get supports for different periods
    supports = get_supports(stock)
    # print(f"Supports for {ticker}: {supports}")
    moving_averages = get_moving_averages(stock)
    # print(f"Moving averages for {ticker}: {moving_averages}")
    
    # Run analysis for buy signals against current price
    buy_signal = check_buy_signal(stock, supports, moving_averages)
    print(f"Buy signal for {ticker}: {buy_signal}")
    
    
    if buy_signal is not None:        
        # Plot stock data with moving average and support/resistance levels
        fig = plot_with_levels(stock, buy_signal)
        captions = generate_captions(buy_signal)
        # Send Telegram message if conditions are met
        save_and_send_plot(fig, f"image_cache\\{ticker}.png", captions)
