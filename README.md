# 📊 Crypto API Tracker Bot

A high-performance asynchronous Telegram bot built with Python and `aiogram` framework. It acts as an automated data pipeline, directly fetching real-time cryptocurrency prices from the core Binance API.

## ⚙️ Features
- **Asynchronous Processing**: Handles multiple user requests simultaneously without blocking via `asyncio` and `aiogram`.
- **Direct API Integration**: Bypasses frontend scraping by interacting directly with the Binance v3 API endpoints (`requests`), ensuring zero breakage from UI updates.
- **Interactive UI**: Custom Reply Keyboard markup for seamless user experience without manual command typing.
- **Secure Environment**: Complete separation of logic and credentials using `python-dotenv`.

## 🛠 Tech Stack
- **Language**: Python 3
- **Framework**: aiogram 3.x
- **Libraries**: requests, python-dotenv, asyncio
- **Data Source**: Binance Official API

## 🚀 Quick Start
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add your bot token: `BOT_TOKEN=your_telegram_token`
4. Run the server: `python main.py`

*Note: This project demonstrates the ability to build stable, API-driven backend microservices.*