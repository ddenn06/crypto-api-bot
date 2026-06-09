import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

from exchanges import get_all_prices
from logic import find_best_spread
from database import create_db, add_user, log_spread

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Сканувати BTC"), KeyboardButton(text="💎 Сканувати ETH")],
        [KeyboardButton(text="📊 Історія спредів"), KeyboardButton(text="⚙️ Налаштування")]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)

    await message.answer(
        f"Привіт, {message.from_user.first_name}! 👋\n\n"
        "Я твій особистий арбітражний сканер. Я моніторю ціни на Binance, WhiteBit, Bybit та KuCoin. "
        "Обери монету, щоб знайти вигідну різницю в курсі.",
        reply_markup=kb
    )

@dp.message(F.text.contains("Сканувати"))
async def scan_market(message: types.Message):
    coin = "BTC" if "BTC" in message.text else "ETH"

    status_msg = await message.answer(f"🔍 Опитую біржі по {coin}... Зачекайте кілька секунд.")

    prices = await get_all_prices(coin)

    result = find_best_spread(prices)

    if not result:
        await status_msg.edit_text("❌ Помилка: Не вдалося отримати дані. Перевір з'єднання з API.")
        return

    if result['percent'] > 0.1:
        log_spread(coin, result['buy_at'], result['sell_at'], result['percent'])

    text = (
        f"<b>📊 Звіт по арбітражу ({coin}):</b>\n\n"
        f"📥 <b>Купити:</b> {result['buy_at']} (${result['buy_price']:,.2f})\n"
        f"📤 <b>Продати:</b> {result['sell_at']} (${result['sell_price']:,.2f})\n\n"
        f"💵 <b>Різниця:</b> ${result['spread_usd']:,.2f}\n"
        f"📈 <b>Профіт:</b> <code>{result['percent']}%</code>\n\n"
        f"✅ <i>Дані збережено в історію для аналізу.</i>"
    )

    await status_msg.edit_text(text, parse_mode="HTML")


async def main():
    create_db()
    print("Арбітражний сканер для друга запущено успішно!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())