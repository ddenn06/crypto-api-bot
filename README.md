# 🚀 Crypto Arbitrage & Tracker Bot

## 📝 Description
A high-performance, asynchronous Telegram bot designed to monitor cryptocurrency markets in real-time and identify profitable arbitrage opportunities. The bot concurrently fetches live pricing data from multiple major exchanges and calculates the best buy/sell spreads, logging all successful finds into a local database.

## ✨ Key Features
* **Real-time Arbitrage Scanning:** Calculates optimal buy and sell points across different platforms.
* **Concurrent API Requests:** Utilizes `aiohttp` to fetch data simultaneously from all exchanges, ensuring zero blocking and lightning-fast responses.
* **Multi-Exchange Integration:** Supports Binance, WhiteBit, Bybit, and KuCoin.
* **Database Logging:** Automatically tracks and saves profitable spread history using SQLite.
* **Secure Configuration:** Environment variables are safely managed via `python-dotenv`.

## 🛠 Tech Stack
* **Language:** Python 3.x
* **Framework:** `aiogram` 3.x (Fully Asynchronous)
* **Networking:** `aiohttp` (Concurrent REST API requests)
* **Database:** SQLite3
* **Security:** `python-dotenv`

## ⚙️ Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ddenn06/your-repo-name.git](https://github.com/ddenn06/your-repo-name.git)
   cd your-repo-name