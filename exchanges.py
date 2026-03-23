import requests

# 1. Binance
def get_binance_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url, timeout=5).json()
        return float(res['price'])
    except:
        return None

# 2. WhiteBit (Українська біржа, часто є спреди)
def get_whitebit_price(symbol="BTC_USDT"):
    try:
        url = f"https://whitebit.com/api/v4/public/ticker"
        res = requests.get(url, timeout=5).json()
        return float(res[symbol]['last_price'])
    except:
        return None

# 3. Bybit
def get_bybit_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        res = requests.get(url, timeout=5).json()
        return float(res['result']['list'][0]['lastPrice'])
    except:
        return None

# 4. KuCoin
def get_kucoin_price(symbol="BTC-USDT"):
    try:
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
        res = requests.get(url, timeout=5).json()
        return float(res['data']['price'])
    except:
        return None

# Головна функція збору
def get_all_prices(coin="BTC"):
    return {
        "Binance": get_binance_price(f"{coin}USDT"),
        "WhiteBit": get_whitebit_price(f"{coin}_USDT"),
        "Bybit": get_bybit_price(f"{coin}USDT"),
        "KuCoin": get_kucoin_price(f"{coin}-USDT")
    }