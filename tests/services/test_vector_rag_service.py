# tests/services/test_vector_rag_service.py

from repositories.vector_repository import VectorRepository

from services.embedding_service import EmbeddingService
from services.vector_search_service import VectorSearchService
from services.llm_service import LlmService
from services.vector_rag_service import VectorRagService


DATABASE_PATH = "data/chatbot.db"

embedding_service = EmbeddingService(
    model="nomic-embed-text"
)

vector_repository = VectorRepository(
    DATABASE_PATH
)

search_service = VectorSearchService(
    embedding_service=embedding_service,
    vector_repository=vector_repository
)

llm_service = LlmService(
    model="llama3.2"
)

rag_service = VectorRagService(
    search_service=search_service,
    llm_service=llm_service
)

# answer = rag_service.ask(
#     "Who created FastAPI?"
# )
answer = rag_service.ask(
    "What kind of framework is FastAPI and who created it?"
)

print("\n" + "=" * 80)
print(answer)
print("=" * 80)