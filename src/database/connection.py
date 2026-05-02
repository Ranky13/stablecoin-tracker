import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None


def close_connection(conn, cur=None):
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()
    except Exception as e:
        print(f"Error occurred while closing cursor: {e}")


def test_connection():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print(f"Connected to PostgreSQL successfully!")
        print(f"Version: {cur.fetchone()[0]}")
        close_connection(conn, cur)
    else:
        print("Connection failed.")


if __name__ == "__main__":
    test_connection()