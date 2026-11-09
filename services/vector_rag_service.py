# services/vector_rag_service.py

from services.vector_search_service import VectorSearchService
from services.llm_service import LlmService


class VectorRagService:

    MIN_SIMILARITY = 0.65
    NO_CONTEXT_FOUND_MESSAGE = (
    "I could not find relevant information "
    "in the knowledge base."
)

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
            print(
                f"Score={result.similarity:.4f} | "
                f"Source={result.chunk.source_document}"
            )

        relevant_results = [
            result
            for result in search_results
            if result.similarity >= self.MIN_SIMILARITY
        ]

        if not relevant_results:
            return self.NO_CONTEXT_FOUND_MESSAGE

        context = "\n\n".join(
            result.chunk.content
            for result in relevant_results
        )

        prompt = f"""
You are a helpful assistant.

Use only the provided context to answer the question.

If the answer cannot be found in the context,
say:
"I could not find relevant information in the knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""

        answer = self._llm_service.generate(prompt)

        return answer