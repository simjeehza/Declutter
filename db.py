import sqlite3

DB_NAME = "media_files.db"

def initialize_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            size INTEGER NOT NULL,
            date_created TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def store_file_metadata(path, size, date_created):
    """Store metadata in the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO files (path, size, date_created) VALUES (?, ?, ?)', (path, size, date_created))
    conn.commit()
    conn.close()

def get_oldest_files(limit=20):
    """Retrieve the 20 oldest files from the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT path, size, date_created FROM files ORDER BY date_created LIMIT ?', (limit,))
    files = c.fetchall()
    conn.close()
    return files
