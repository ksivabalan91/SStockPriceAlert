import yfinance as yf
import datetime
from TelegramMsg import send_telegram_message
from Stock import Stock
from Supports import get_supports


tickers = ['PLTR','NVDA','VOO','AMD','AAPL','AMZN','GOOG','MSFT','BTC-USD','ETH-USD']
# tickers = ['NVDA']

for ticker in tickers:
    # Initialize Stock object
    stock = Stock(ticker)
    # Get supports for different periods
    supports = get_supports(stock)
    print(f"Supports for {ticker}: {supports}")
    # Run analysis for buy signals

    # Plot stock data with moving average and support/resistance levels

    # Send Telegram message if conditions are met
    # send_telegram_message(f'Running job now, @ {datetime.datetime.now()}')






