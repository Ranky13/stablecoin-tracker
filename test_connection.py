import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    cur = conn.cursor()
    
    # Test connection
    cur.execute("SELECT version();")
    print("Connected to PostgreSQL successfully!")
    print(f"Version: {cur.fetchone()[0]}")
    
    # Check all five tables exist
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cur.fetchall()
    print("\n Tables found in database:")
    for table in tables:
        print(f"   {table[0]}")

    cur.close()
    conn.close()
    print("\n Everything is set up correctly!")

except Exception as e:
    print(f" Connection failed: {e}")