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
def get_or_create_conversation(session_id):
    conn = get_connection()
    cur = conn.cursor()

    # Check if conversation already exists
    cur.execute(
        "SELECT id FROM conversations WHERE session_id = %s;",
        (session_id,)
    )
    conversation = cur.fetchone()

    if conversation:
        conversation_id = conversation[0]
    else:
        user_id = get_default_user()

        cur.execute(
            """
            INSERT INTO conversations (user_id, session_id)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (user_id, session_id)
        )

        conversation_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    return conversation_id

def save_message(conversation_id, role, message):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO messages (conversation_id, role, message)
        VALUES (%s, %s, %s);
        """,
        (conversation_id, role, message)
    )

    conn.commit()

    cur.close()
    conn.close()
