import json
import sqlite3

from models.chat_models import DocumentChunk

class VectorRepository:

    def __init__(self, database_path: str):
        self.database_path = database_path

    def save_chunk(self, chunk: DocumentChunk):
        connection = sqlite3.connect(self.database_path)
        connection.execute(
            """
            INSERT INTO document_chunks
            (source_document, content, embedding)
            VALUES (?, ?, ?)
            """,
            (
                chunk.source_document,
                chunk.content,
                json.dumps(chunk.embedding)
            )
        )

        connection.commit()
        connection.close()

    def get_all_chunks(self):

        connection = sqlite3.connect(self.database_path)
        rows = connection.execute(
            """
            SELECT id,
                source_document,
                content,
                embedding
            FROM document_chunks
            """
        ).fetchall()

        connection.close()
        chunks = []
        for row in rows:
            chunks.append(
                DocumentChunk(
                    id=row[0],
                    source_document=row[1],
                    content=row[2],
                    embedding=json.loads(row[3])
                )
            )
        return chunks