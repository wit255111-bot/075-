import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'techhub.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL, -- 'hardware' or 'software'
            brand TEXT NOT NULL,
            price REAL NOT NULL,
            original_price REAL,
            stock INTEGER DEFAULT 10,
            image_url TEXT,
            description TEXT,
            specs_json TEXT, -- JSON attributes for compatibility & display
            warranty TEXT,
            rating REAL DEFAULT 4.8,
            is_featured INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_address TEXT,
            delivery_type TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            total_amount REAL NOT NULL,
            items_json TEXT NOT NULL,
            digital_keys_json TEXT,
            status TEXT DEFAULT 'Processing',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully at", DB_PATH)
