from repositories.document_repository import DocumentRepository
from repositories.vector_repository import VectorRepository

from services.embedding_service import EmbeddingService
from services.document_loader_service import (
    DocumentLoaderService
)

loader = DocumentLoaderService(
    document_repository=DocumentRepository(),
    vector_repository=VectorRepository(
        "data/chatbot.db"
    ),
    embedding_service=EmbeddingService(
        model="nomic-embed-text"
    )
)

loader.load_documents()

print("Finished")