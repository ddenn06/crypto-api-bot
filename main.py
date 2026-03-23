import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Імпорт твоїх модулів
from database import create_db, add_user, get_all_users, log_spread
from exchanges import get_all_prices
from logic import find_best_spread

# 1. Налаштування
load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# 2. Головне меню (UI)
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Курси Binance"), KeyboardButton(text="🚀 Арбітражний сканер")],
        [KeyboardButton(text="ℹ️ Можливості"), KeyboardButton(text="👥 База юзерів")],
        [KeyboardButton(text="🔄 Перезапуск")]
    ],
    resize_keyboard=True
)


# 4. Хендлер Старту
@dp.message(CommandStart())
@dp.message(F.text == "🔄 Перезапуск")
async def start_handler(message: types.Message):
    add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer(
        f"Вітаю, {message.from_user.first_name}! Систему активовано.\n"
        "Обери функцію в меню нижче:",
        reply_markup=main_kb
    )


# 5. Хендлер Курсів (Твій перший код)
@dp.message(F.text == "📊 Курси Binance")
async def crypto_tracker_handler(message: types.Message):
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        btc = float(requests.get(url, params={"symbol": "BTCUSDT"}).json()["price"])
        eth = float(requests.get(url, params={"symbol": "ETHUSDT"}).json()["price"])
        await message.answer(f"🪙 <b>BTC:</b> ${btc:,.2f}\n💠 <b>ETH:</b> ${eth:,.2f}", parse_mode="HTML")
    except:
        await message.answer("Помилка API Binance.")


# 6. АРБІТРАЖНИЙ СКАНЕР (Код для друга)
@dp.message(F.text == "🚀 Арбітражний сканер")
async def arbitrage_handler(message: types.Message):
    status = await message.answer("🔍 Аналізую Binance, WhiteBit, Bybit та KuCoin...")

    prices = get_all_prices("BTC")
    res = find_best_spread(prices)

    if res:
        if res['percent'] > 0.05:
            log_spread("BTC", res['buy_at'], res['sell_at'], res['percent'])

        text = (
            f"<b>💰 Знайдено спред (BTC):</b>\n\n"
            f"📥 Купити: {res['buy_at']} (${res['buy_price']:,.2f})\n"
            f"📤 Продати: {res['sell_at']} (${res['sell_price']:,.2f})\n\n"
            f"📈 Профіт: <code>{res['percent']}%</code> (${res['spread_usd']})"
        )
        await status.edit_text(text, parse_mode="HTML")
    else:
        await status.edit_text("Не вдалося отримати дані з усіх бірж.")


# 7. Адмін-панель (Користувачі)
@dp.message(F.text == "👥 База юзерів")
@dp.message(Command("users"))
async def admin_users(message: types.Message):
    users = get_all_users()
    if not users:
        await message.answer("База порожня.")
        return
    text = "👥 <b>Користувачі:</b>\n\n"
    for u in users:
        text += f"👤 {u[0]} (@{u[1]}) - {u[2]}\n"
    await message.answer(text, parse_mode="HTML")


# 8. Можливості
@dp.message(F.text == "ℹ️ Можливості")
async def info_handler(message: types.Message):
    await message.answer(
        "🛠 <b>Цей бот вміє:</b>\n"
        "1. Моніторити ціни в реальному часі.\n"
        "2. Шукати арбітражні вікна між 4 біржами.\n"
        "3. Зберігати історію спредів та базу користувачів у SQLite.",
        parse_mode="HTML"
    )


# 9. Запуск
async def main():
    create_db()
    print("Супер-бот запущений!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())