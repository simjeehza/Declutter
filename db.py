import sqlite3

# Initialize the database
def initialize_db():
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            size INTEGER NOT NULL,
            date_created TEXT NOT NULL,
            status INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Store file metadata in the database
def store_file_metadata(path, size, date_created, status=0):
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO files (path, size, date_created, status)
        VALUES (?, ?, ?, ?)
    ''', (path, size, date_created, status))
    conn.commit()
    conn.close()

# Fetch files based on status (e.g., for review)
def get_oldest_files(batch_size=20, offset=0, status=0):
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('''
        SELECT path, size, date_created FROM files
        WHERE status = ?
        ORDER BY date_created ASC
        LIMIT ? OFFSET ?
    ''', (status, batch_size, offset))
    files = c.fetchall()
    conn.close()
    return files

# Update the status of a file (for marking as deletion or skipped)
def update_file_status(file_path, new_status):
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('''
        UPDATE files
        SET status = ?
        WHERE path = ?
    ''', (new_status, file_path))
    conn.commit()
    conn.close()
