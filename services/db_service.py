import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn_string = "host=localhost port=5432 dbname=teckia_db user=teckia_user password=teckia2024"
    return psycopg2.connect(conn_string)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translations (
            id          SERIAL PRIMARY KEY,
            source_lang VARCHAR(10)  NOT NULL,
            target_lang VARCHAR(10)  NOT NULL,
            input_text  TEXT         NOT NULL,
            output_text TEXT         NOT NULL,
            is_favorite BOOLEAN      DEFAULT FALSE,
            created_at  TIMESTAMP    DEFAULT NOW()
        );
    """)
    # Ajouter colonne is_favorite si elle n'existe pas (migration)
    cursor.execute("""
        ALTER TABLE translations 
        ADD COLUMN IF NOT EXISTS is_favorite BOOLEAN DEFAULT FALSE;
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Base de données initialisée.")

def save_translation(source_lang, target_lang, input_text, output_text):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        INSERT INTO translations (source_lang, target_lang, input_text, output_text)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """, (source_lang, target_lang, input_text, output_text))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return dict(result) if result else None

def get_history(limit=50, favorites_only=False):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if favorites_only:
        cursor.execute("""
            SELECT * FROM translations
            WHERE is_favorite = TRUE
            ORDER BY created_at DESC
            LIMIT %s;
        """, (limit,))
    else:
        cursor.execute("""
            SELECT * FROM translations
            ORDER BY created_at DESC
            LIMIT %s;
        """, (limit,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    history = []
    for row in results:
        item = dict(row)
        if item.get('created_at'):
            item['created_at'] = item['created_at'].isoformat()
        history.append(item)
    return history

def toggle_favorite(translation_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        UPDATE translations 
        SET is_favorite = NOT is_favorite 
        WHERE id = %s
        RETURNING is_favorite;
    """, (translation_id,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return dict(result) if result else None

def delete_translation(translation_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM translations WHERE id = %s;", (translation_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    cursor.close()
    conn.close()
    return deleted