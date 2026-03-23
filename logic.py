def find_best_spread(prices):
    # Очищаємо дані від помилок (None)
    clean_prices = {k: v for k, v in prices.items() if v is not None}

    if len(clean_prices) < 2:
        return None

    # Знаходимо мінімальну та максимальну ціну
    min_exchange = min(clean_prices, key=clean_prices.get)
    max_exchange = max(clean_prices, key=clean_prices.get)

    buy_price = clean_prices[min_exchange]
    sell_price = clean_prices[max_exchange]

    # Рахуємо різницю
    spread_usd = sell_price - buy_price
    percent = (spread_usd / buy_price) * 100

    return {
        "buy_at": min_exchange,
        "sell_at": max_exchange,
        "buy_price": buy_price,
        "sell_price": sell_price,
        "spread_usd": round(spread_usd, 2),
        "percent": round(percent, 2)
    }