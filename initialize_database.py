from psycopg2 import connect
from dotenv import load_dotenv
import os

load_dotenv()

conn = connect(
    host = "localhost",
    user = os.getenv("DB_USER") or "postgres",
    password = os.getenv("DB_PASSWORD") or "postgres",
    database = os.getenv("DB_NAME") or "wallet_management"
)

with conn.cursor() as cur:
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
    conn.commit()
    print("created table users")

    cur.execute("CREATE TABLE IF NOT EXISTS wallet (user_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE, balance FLOAT DEFAULT 0)")
    conn.commit()
    print("created table wallet")

    cur.execute("CREATE TABLE IF NOT EXISTS purchases (product_id SERIAL PRIMARY KEY, user_id INT NOT NULL REFERENCES users(user_id), product_name TEXT NOT NULL, product_price FLOAT, purchase_date TIMESTAMP DEFAULT NOW())")
    conn.commit()
    print("created table purchases")

conn.close()