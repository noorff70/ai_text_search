from repositories.vector_repository import VectorRepository
from services.embedding_service import EmbeddingService
from services.vector_search_service import VectorSearchService

DATABASE_PATH = "data/chatbot.db"

embedding_service = EmbeddingService(
    model="nomic-embed-text"
)

repository = VectorRepository(
    DATABASE_PATH
)

search_service = VectorSearchService(
    embedding_service=embedding_service,
    vector_repository=repository
)

results = search_service.vector_search(
    "What is FastAPI?",
    top_k=5
)

for result in results:

    print("\n" + "=" * 80)
    print(f"Similarity: {result.similarity:.4f}")
    print(f"Source: {result.chunk.source_document}")
    print()
    print(result.chunk.content)
