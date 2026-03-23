import sqlite3

def create_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    # Таблиця користувачів
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Таблиця історії арбітражу
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spread_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin TEXT,
            buy_at TEXT,
            sell_at TEXT,
            percent REAL,
            found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_user(telegram_id, username, first_name):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (telegram_id, username, first_name) VALUES (?, ?, ?)',
                   (telegram_id, username, first_name))
    conn.commit()
    conn.close()

def log_spread(coin, buy_at, sell_at, percent):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO spread_history (coin, buy_at, sell_at, percent) VALUES (?, ?, ?, ?)',
                   (coin, buy_at, sell_at, percent))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, username, join_date FROM users")
    users = cursor.fetchall()
    conn.close()
    return users