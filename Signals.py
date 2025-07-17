from Stock import Stock

def check_buy_signal(stock: Stock, supports: list[float], moving_average: dict)-> dict | None:
    current_price = [stock.current_high, stock.current_low, stock.current_open, stock.current_close]
    signal = {
        'ticker': stock.ticker,
        'score': 0,
        'current_price': current_price[-1]
    }

    for support in supports:
        for price in current_price:
            if abs(price - support) / support * 100 <= 3:
                signal['score'] += 1                
                if 'support_level' not in signal:
                    signal['support_level'] = []
                signal['support_level'].append(support)
                break
    for ma_key, (ma_value, weight) in moving_average.items():
        for price in current_price:
            if abs(price - ma_value) / ma_value * 100 <= 3:
                signal['score'] += weight
                if 'moving_average' not in signal:
                    signal['moving_average'] = {}
                signal['moving_average'][ma_key] = ma_value
                break
    if signal['score'] >= 1.5:
        return signal    
    return None