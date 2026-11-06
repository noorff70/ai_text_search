from services.embedding_service import EmbeddingService
from repositories.vector_repository import VectorRepository

from models.chat_models import SearchResult
from utilities.vector_utils import cosine_similarity

# The code defines a VectorSearchService class that performs semantic text searching using vector embeddings and cosine similarity. Instead of matching exact keywords, it finds information based on the conceptual meaning of a user's query.

class VectorSearchService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_repository: VectorRepository
    ):
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository

    def vector_search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[SearchResult]:

        query_embedding = (
            self.embedding_service.embed(query)
        )

        chunks = self.vector_repository.get_all_chunks()
        scored_chunks = []

        for chunk in chunks:
            similarity = (
                cosine_similarity(
                    query_embedding,
                    chunk.embedding
                )
            )
            scored_chunks.append(
                SearchResult(
                    chunk=chunk,
                    similarity=similarity
                )
            )
        scored_chunks.sort(
            key=lambda x: x.similarity,
            reverse=True
        )
        
        return scored_chunks[:top_k]