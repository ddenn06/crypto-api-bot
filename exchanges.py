import aiohttp
import asyncio


async def get_binance_price(session, symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        async with session.get(url, timeout=5) as response:
            res = await response.json()
            return float(res['price'])
    except Exception:
        return None


async def get_whitebit_price(session, symbol="BTC_USDT"):
    url = f"https://whitebit.com/api/v4/public/ticker"
    try:
        async with session.get(url, timeout=5) as response:
            res = await response.json()
            return float(res[symbol]['last_price'])
    except Exception:
        return None


async def get_bybit_price(session, symbol="BTCUSDT"):
    url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
    try:
        async with session.get(url, timeout=5) as response:
            res = await response.json()
            return float(res['result']['list'][0]['lastPrice'])
    except Exception:
        return None


async def get_kucoin_price(session, symbol="BTC-USDT"):
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
    try:
        async with session.get(url, timeout=5) as response:
            res = await response.json()
            return float(res['data']['price'])
    except Exception:
        return None


async def get_all_prices(coin="BTC"):
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_binance_price(session, f"{coin}USDT"),
            get_whitebit_price(session, f"{coin}_USDT"),
            get_bybit_price(session, f"{coin}USDT"),
            get_kucoin_price(session, f"{coin}-USDT")
        ]

        results = await asyncio.gather(*tasks)

        return {
            "Binance": results[0],
            "WhiteBit": results[1],
            "Bybit": results[2],
            "KuCoin": results[3]
        }