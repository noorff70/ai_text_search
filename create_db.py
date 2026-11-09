# create_db.py

import sqlite3

DATABASE_PATH = "data/chatbot.db"

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Drop existing tables
cursor.execute("DROP TABLE IF EXISTS message")
cursor.execute("DROP TABLE IF EXISTS conversation")
cursor.execute("DROP TABLE IF EXISTS document_chunks")

# Create conversation table
cursor.execute("""
CREATE TABLE conversation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Create message table
cursor.execute("""
CREATE TABLE message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(conversation_id) REFERENCES conversation(id)
)
""")

# Create document_chunks table
cursor.execute("""
CREATE TABLE document_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_document TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database recreated successfully.")