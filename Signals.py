from Stock import Stock
import matplotlib.pyplot as plt

def check_buy_signal(stock: Stock, supports: list[float], moving_average: dict):
    current_price = stock.current_price
    signals = {
        'score': 0,
        'support_level': [],
        'moving_average': {},
    }

    for support in supports:
        if abs(current_price - support) / support * 100 <= 5.0:
            signals['score'] += 1
            signals['support_level'].append(support)
    for ma_key, (ma_value, weight) in moving_average.items():
        if abs(current_price - ma_value) / ma_value * 100 <= 5.0:
            signals['score'] += weight
            signals['moving_average'][ma_key] = ma_value

    if signals['score'] >= 0.5:
        return signals
    
    return None

def plot_with_levels(stock: Stock, buy_signal):
    pass