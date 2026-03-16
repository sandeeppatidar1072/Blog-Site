import sqlite3

# create database
db = sqlite3.connect("database.db")
cursor = db.cursor()

# BLOG TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS blogs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
description TEXT,
image TEXT
)
""")

# PRODUCT TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
price INTEGER,
description TEXT,
image TEXT
)
""")

# CART TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
id INTEGER PRIMARY KEY AUTOINCREMENT,
product_id INTEGER,
quantity INTEGER
)
""")

db.commit()
db.close()

print("Database and tables created successfully")