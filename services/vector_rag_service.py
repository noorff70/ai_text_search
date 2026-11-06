# services/vector_rag_service.py

from services.vector_search_service import VectorSearchService
from services.llm_service import LlmService


class VectorRagService:

    def __init__(
        self,
        search_service: VectorSearchService,
        llm_service: LlmService
    ):
        self._search_service = search_service
        self._llm_service = llm_service

    def ask(
        self,
        question: str,
        top_k: int = 5
    ):

        search_results = self._search_service.vector_search(
            query=question,
            top_k=top_k
        )

        # TODO: temporarily adding for testing.
        for result in search_results:
            print(f"\nScore: {result.similarity:.4f}")
            print(f"Document: "f"{result.chunk.source_document}")
            print(result.chunk.content)

        context = "\n\n".join(
            result.chunk.content
            for result in search_results
        )

        prompt = f"""
You are a helpful assistant.

Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

        answer = self._llm_service.generate(prompt)

        return answer