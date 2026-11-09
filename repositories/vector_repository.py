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
            (
                source_document,
                chunk_index,
                content,
                embedding
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                chunk.source_document,
                chunk.chunk_index,
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
            SELECT
                id,
                source_document,
                chunk_index,
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
                    chunk_index=row[2],
                    content=row[3],
                    embedding=json.loads(row[4])
                )
            )

        return chunks