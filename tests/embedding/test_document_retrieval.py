from services.embedding_service import EmbeddingService
from services.document_retrieval_service import (
    DocumentRetrievalService
)

embedding_service = EmbeddingService(
    "nomic-embed-text"
)

retrieval_service = DocumentRetrievalService(
    embedding_service
)

result = retrieval_service.get_best_document_with_score(
    "How do I create a REST API?"
)

print(result["document"]["name"])
print(result["score"])
