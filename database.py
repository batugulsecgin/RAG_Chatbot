import sqlite3
import re

DB_NAME = "chatbot_data.db"


def init_db():
    """Veritabanını ve arama tablosunu oluşturur."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # FTS5 (Tam Metin Arama) kullanarak hızlı arama yapabileceğimiz sanal tablo
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_base 
        USING fts5(title, content)
    ''')

    conn.commit()
    conn.close()


def insert_knowledge(title, content):
    """Veritabanına yeni bir bilgi/belge ekler."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO knowledge_base (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()


def search_knowledge(user_query, limit=3):
    """Kullanıcının sorusundaki kelimeleri veritabanında arar."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Sorudaki özel karakterleri temizle (FTS5 syntax hatasını önlemek için)
    clean_query = re.sub(r'[^\w\s]', '', user_query).strip()

    # Kelimeleri 'OR' mantığıyla birleştirerek eşleşme şansını artırıyoruz
    search_term = " OR ".join(clean_query.split())

    try:
        cursor.execute('''
                       SELECT title, content
                       FROM knowledge_base
                       WHERE knowledge_base MATCH ?
                       ORDER BY rank LIMIT ?
                       ''', (search_term, limit))
        results = cursor.fetchall()
    except sqlite3.Error:
        results = []

    conn.close()
    return results


if __name__ == "__main__":
    init_db()
    print("Veritabanı 'chatbot_data.db' başarıyla oluşturuldu!")