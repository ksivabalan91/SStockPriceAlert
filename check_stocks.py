import yfinance as yf
import requests
import os
import datetime


tickers = ['PLTR','NVDA','VOO','AMD','AAPL','AMZN','GOOG','MSFT','BTC-USD','ETH-USD']
threshold_pct = 5
chat_id = os.getenv('TELEGRAM_CHAT_ID')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')


def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, json=payload)
    return response.json()

def check_moving_average(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='5y', interval='1wk')

    current_price = hist['Close'].iloc[-1]
    ma200 = hist['Close'].rolling(window=100).mean().iloc[-1]

    if ma200 == 0 or ma200 is None:
        return  # Avoid division by zero

    diff_pct = abs(current_price - ma200) / ma200 * 100
    if diff_pct <= threshold_pct:
        msg = f"📈 {ticker} is near its 200-week MA: {current_price:.2f} vs MA {ma200:.2f} ({diff_pct:.2f}%)"
        send_telegram_message(msg)

send_telegram_message(f'Running job now, @ {datetime.datetime.now()}')
for ticker in tickers:
    check_moving_average(ticker)
