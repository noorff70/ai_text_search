from pathlib import Path

from services.embedding_service import EmbeddingService
from repositories.vector_repository import VectorRepository
from models.chat_models import DocumentChunk
from utilities.text_chunker import chunk_text

embedding_service = EmbeddingService(
    model="nomic-embed-text"
)
repository = VectorRepository("data/chatbot.db")

text = Path("data/documents/fastapi.txt").read_text()

chunks = chunk_text(text)

for chunk in chunks:

    vector = embedding_service.embed(chunk)

    repository.save_chunk(
        DocumentChunk(
            id=None,
            source_document="fastapi.txt",
            content=chunk,
            embedding=vector
        )
    )

print("Finished")