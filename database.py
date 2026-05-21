import sqlite3
from datetime import datetime

DB_NAME = "bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, height INTEGER, target_calories INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS weight_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, weight REAL, date TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS food_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, calories INTEGER, description TEXT, date TEXT)')
    conn.commit()
    conn.close()

def log_weight(user_id, weight):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weight_logs (user_id, weight, date) VALUES (?, ?, ?)", (user_id, weight, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def log_food(user_id, calories, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO food_logs (user_id, calories, description, date) VALUES (?, ?, ?, ?)", (user_id, calories, description, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_today_calories(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT SUM(calories) FROM food_logs WHERE user_id = ? AND date = ?", (user_id, today))
    res = cursor.fetchone()[0]
    conn.close()
    return res if res else 0
