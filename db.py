import os
from dotenv import load_dotenv
import psycopg

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def get_default_user():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id = 1;")
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return user[0]

    return None