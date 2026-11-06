# tests/vector/check_chunks.py

import sqlite3

connection = sqlite3.connect("data/chatbot.db")

rows = connection.execute("""
    SELECT id,
           source_document,
           content
    FROM document_chunks
""").fetchall()

for row in rows:
    print()
    print(f"ID: {row[0]}")
    print(f"Source: {row[1]}")
    print(f"Content: {row[2]}")

connection.close()