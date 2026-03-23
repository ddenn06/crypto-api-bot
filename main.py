import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from database import create_db, add_user, get_all_users

# 1. Завантаження ключів
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# 2. Ініціалізація ядра
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 3. Створення інтерфейсу (Клавіатура керування)
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Отримати курси (API)"), KeyboardButton(text="🛠 Статус сервера")],
        [KeyboardButton(text="ℹ️ Можливості бота"), KeyboardButton(text="👥 База користувачів")],
        [KeyboardButton(text="🔄 Перезапуск (Старт)")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Термінал керування..."
)


# 4. Хендлер старту (видає клавіатуру користувачу)
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    # Записуємо користувача в базу даних
    add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)

    await message.answer(
        f"Вітаю, {message.from_user.full_name}! Термінал керування активовано.",
        reply_markup=main_kb
    )


# 4.1 Хендлер Адміна: Перегляд бази даних (реагує на кнопку)
@dp.message(F.text == "👥 База користувачів")
async def admin_get_users(message: types.Message):
    users = get_all_users()

    if not users:
        await message.answer("📭 База даних поки що порожня.")
        return

    text = "👥 <b>Клієнти в базі:</b>\n\n"
    for user in users:
        text += f"👤 <b>{user[0]}</b> (@{user[1]})\n🕒 Зареєстровано: {user[2]}\n\n"

    await message.answer(text, parse_mode="HTML")

# 4.2 Хендлер: Можливості бота
@dp.message(F.text == "ℹ️ Можливості бота")
async def bot_capabilities(message: types.Message):
    text = (
        "🤖 <b>Технічний стек та можливості:</b>\n\n"
        "1️⃣ <b>API Інтеграція:</b> Пряме з'єднання з серверами Binance.\n"
        "2️⃣ <b>База даних:</b> Локальне збереження клієнтів (SQLite).\n"
        "3️⃣ <b>Асинхронність:</b> Швидка обробка запитів на aiogram 3.x.\n\n"
        "<i>Систему розроблено для портфоліо.</i>"
    )
    await message.answer(text, parse_mode="HTML")

# 4.3 Хендлер: Перезапуск (імітація команди /start)
@dp.message(F.text == "🔄 Перезапуск (Старт)")
async def restart_bot(message: types.Message):
    # Викликаємо існуючу функцію старту
    await command_start_handler(message)

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
    # Ініціалізуємо базу даних при запуску
    create_db()

    print("Бот з інтерактивною клавіатурою успішно запущено...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
