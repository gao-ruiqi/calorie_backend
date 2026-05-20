import sqlite3
import datetime
import os

DB_NAME = "calorie.db"

# 初始化数据库，建表
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS user
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  goal TEXT)''')

    # 饮食记录表
    c.execute('''CREATE TABLE IF NOT EXISTS diet_record
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  device_id TEXT,
                  weight REAL,
                  food_name TEXT,
                  calorie REAL,
                  protein REAL,
                  carbs REAL,
                  fat REAL,
                  create_time TEXT)''')

    conn.commit()
    conn.close()

# 保存饮食记录
def save_diet_record(device_id, weight, food_name, calorie, protein, carbs, fat):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO diet_record
                 (device_id, weight, food_name, calorie, protein, carbs, fat, create_time)
                 VALUES (?,?,?,?,?,?,?,?)''',
              (device_id, weight, food_name, calorie, protein, carbs, fat, time_now))
    conn.commit()
    conn.close()

# 获取用户今日饮食
def get_today_records():
    today = datetime.date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM diet_record WHERE create_time LIKE ?", (today + "%",))
    data = c.fetchall()
    conn.close()
    return data

# 获取所有记录
def get_all_records():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM diet_record ORDER BY create_time DESC")
    data = c.fetchall()
    conn.close()
    return data

# 初始化表
init_db()