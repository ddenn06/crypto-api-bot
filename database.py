import sqlite3


def create_db():
    # Підключаємося до файлу бази (якщо його немає, Python сам його створить)
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Створюємо таблицю 'users', якщо її ще не існує
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       telegram_id
                       INTEGER
                       UNIQUE,
                       username
                       TEXT,
                       first_name
                       TEXT,
                       join_date
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')

    conn.commit()
    conn.close()
    print("База даних ініціалізована. Таблиця users готова.")


def add_user(telegram_id, username, first_name):
    """Функція для запису нового клієнта в базу"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # INSERT OR IGNORE означає: якщо такий telegram_id вже є, не створювати дублікат
    cursor.execute('''
                   INSERT
                   OR IGNORE INTO users (telegram_id, username, first_name)
        VALUES (?, ?, ?)
                   ''', (telegram_id, username, first_name))

    conn.commit()
    conn.close()


def get_all_users():
    """Функція для витягування списку клієнтів з бази"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Витягуємо ім'я, нікнейм та дату реєстрації
    cursor.execute("SELECT first_name, username, join_date FROM users")
    users = cursor.fetchall()  # Отримуємо всі рядки

    conn.close()
    return users