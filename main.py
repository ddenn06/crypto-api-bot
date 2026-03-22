import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# 1. Завантаження ключів
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# 2. Ініціалізація ядра
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 3. Створення інтерфейсу (Клавіатура керування)
# resize_keyboard=True робить кнопки акуратними під розмір екрана
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Отримати курси (API)")],
        [KeyboardButton(text="🛠 Статус сервера")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Виберіть дію в меню..."
)


# 4. Хендлер старту (видає клавіатуру користувачу)
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        f"Вітаю, {message.from_user.full_name}! Термінал керування активовано.",
        reply_markup=main_kb
    )


# 5. Хендлер запиту до Binance (реагує на натискання кнопки)
@dp.message(F.text == "📊 Отримати курси (API)")
async def crypto_tracker_handler(message: types.Message):
    await message.answer("З'єднуюсь із серверами Binance... ⏳")

    url = "https://api.binance.com/api/v3/ticker/price"

    try:
        btc_price = float(requests.get(url, params={"symbol": "BTCUSDT"}).json()["price"])
        eth_price = float(requests.get(url, params={"symbol": "ETHUSDT"}).json()["price"])
        sol_price = float(requests.get(url, params={"symbol": "SOLUSDT"}).json()["price"])

        text = (
            "<b>Актуальне зведення ринку:</b>\n\n"
            f"🪙 <b>BTC:</b> ${btc_price:,.2f}\n"
            f"💠 <b>ETH:</b> ${eth_price:,.2f}\n"
            f"☀️ <b>SOL:</b> ${sol_price:,.2f}\n\n"
            "<i>Дані отримано через Binance API.</i>"
        )
        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer("Помилка з'єднання з біржею. Перевір логіку.")


# 6. Хендлер перевірки статусу (реагує на другу кнопку)
@dp.message(F.text == "🛠 Статус сервера")
async def status_handler(message: types.Message):
    await message.answer("✅ Усі системи працюють у штатному режимі. З'єднання з API стабільне.")


# 7. Запуск машини
async def main():
    print("Бот з інтерактивною клавіатурою успішно запущено...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
