import psycopg
from psycopg.rows import dict_row
from config import dbname, user, password, host
import asyncio


def connection():
    
    return psycopg.connect(dbname = dbname,
                            user = user,
                            password = password,
                            host = host,
                            port = 5432,row_factory=dict_row)

def init_db():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            note_id BIGINT,
            text TEXT,
            is_done BOOLEAN DEFAULT FALSE,
            da_te TIMESTAMP
        )
    """))
    conn.commit()
    cursor.close()
    conn.close()

def add_note(user_id, text): #create note

    conn = connection()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT COALESCE(MAX(note_id), 0) FROM notes WHERE user_id = %s", (user_id,))
    max_index = cursor.fetchone()["coalesce"]
    new_id = max_index + 1 #Выбираем максимальную по индексу заметку и добавляем к индексу +1 перед созданием новой
    
    
    
    cursor.execute("INSERT INTO notes (user_id, note_id, text, is_done, da_te) VALUES (%s,%s,%s, FALSE, CURRENT_TIMESTAMP)",(user_id,new_id,text))
    conn.commit()
    cursor.close()
    conn.close()

def get_notes(user_id): #get list of notes
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT note_id, text, is_done, da_te FROM notes WHERE user_id = %s ORDER BY note_id", (user_id,))
    notes = cursor.fetchall()
    print (notes)
    cursor.close()
    conn.close()
    return notes

def done_task(user_id, note_id): #crossed task
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE notes
                   SET is_done = NOT is_done 
                   WHERE user_id = %s AND note_id = %s
                   RETURNING is_done, text
                   """, (user_id, note_id))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result

def delete_notes(user_id, note_id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE user_id = %s AND note_id = %s" ,(user_id, note_id))
    
    cursor.execute("""UPDATE notes
                   SET note_id = note_id - 1 
                   WHERE user_id = %s AND note_id > %s
                   """, (user_id,note_id))
    conn.commit()
    cursor.close()
    conn.close()