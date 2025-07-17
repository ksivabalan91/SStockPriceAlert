import yfinance as yf
import pandas as pd

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self._daily_hist = None    # Use underscores for "private" attributes
        self._weekly_hist = None
        self._monthly_hist = None
        self.current_close = None  # Will be set when daily_hist is loaded
        self.current_open = None
        self.current_low = None
        self.current_high = None
        self.supports = []

    def _fetch_history(self, interval):
        """Helper to fetch history with error handling."""
        try:
            hist = self.stock.history(period='10y', interval=interval)
            if hist.empty:
                print(f"Warning: No data found for {self.ticker} with interval {interval}.")
                return pd.DataFrame()
            return hist
        except Exception as e:
            print(f"Error fetching {interval} history for {self.ticker}: {e}")
            return pd.DataFrame()

    @property
    def daily_hist(self):
        if self._daily_hist is None:
            self._daily_hist = self._fetch_history('1d')
            if not self._daily_hist.empty:
                self.current_close = self._daily_hist['Close'].iloc[-1]
                self.current_open = self._daily_hist['Open'].iloc[-1]
                self.current_low = self._daily_hist['Low'].iloc[-1]
                self.current_high = self._daily_hist['High'].iloc[-1]
        return self._daily_hist

    @property
    def weekly_hist(self):
        if self._weekly_hist is None:
            self._weekly_hist = self._fetch_history('1wk')
        return self._weekly_hist

    @property
    def monthly_hist(self):
        if self._monthly_hist is None:
            self._monthly_hist = self._fetch_history('1mo')
        return self._monthly_hist

    def __repr__(self):
        return f"Stock(ticker='{self.ticker}', current_price={self.current_price})"
