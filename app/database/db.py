import psycopg2
from config import user, dbname,password, host
from psycopg2.extras import RealDictCursor

def connection():
    
    return psycopg2.connect(database = dbname, user = user, password = password, host = host, port = 5432,cursor_factory=RealDictCursor)

def init_db():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            text TEXT
        )
    """))
    conn.commit()
    cursor.close()
    conn.close()

def add_note(user_id, text): #create note

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (user_id, text) VALUES (%s,%s)",(user_id,text))
    conn.commit()
    cursor.close()
    conn.close()

def get_notes(user_id): #get list of notes
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM notes WHERE user_id = %s ORDER BY id", (user_id,))
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return notes

def delete_notes(user_id, note_id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE user_id = %s AND id = %s" ,(user_id, note_id))
    conn.commit()
    cursor.close()
    conn.close()
