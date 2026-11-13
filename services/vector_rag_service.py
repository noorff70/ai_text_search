# services/vector_rag_service.py

from services.vector_search_service import VectorSearchService
from services.llm_service import LlmService
from prompts.rag_prompts import (
    RAG_PROMPT,
    QUERY_REWRITE_PROMPT
)

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
        conversation_history: list[dict] | None = None,
        top_k: int = 5
    ):

        effective_question = question

        if conversation_history:
            effective_question = self._rewrite_question(
                    question,
                    conversation_history
                )
        

        print(
            f"\nRewritten Question: "
            f"{effective_question}\n"
        )

        search_results = self._search_service.vector_search(
            query=effective_question,
            top_k=top_k
        )

        # TODO: temporarily adding for testing.
        for result in search_results:
            print(
                f"Score={result.similarity:.4f} | "
                f"Source={result.chunk.source_document} | "
                f"Chunk={result.chunk.chunk_index}"
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

        print("\n===== CONTEXT =====")
        print(context)
        print("===================\n")

        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        answer = self._llm_service.generate(prompt)

        return answer

    # Query rewrite helper
    def _rewrite_question(
        self,
        question: str,
        conversation_history: list[dict]) -> str:

        if not conversation_history:
            return question

        history = "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history[-6:]
        )
        
        rewrite_prompt = QUERY_REWRITE_PROMPT.format(
            history=history,
            question=question
        )

        rewritten_question = (
            self._llm_service.generate(
                rewrite_prompt
            ).strip()
        )

        print("\n===== QUERY REWRITE =====")
        print("Original:", question)
        print("Rewritten:", rewritten_question)
        print("=========================\n")

        return rewritten_question

    def stream(
        self,
        question: str,
        conversation_history: list[dict] | None = None,
        top_k: int = 5
    ):
        effective_question = question
        
        if conversation_history:
            effective_question = self._rewrite_question(
                    question,
                    conversation_history
                )
                
        
        print(
            f"\nRewritten Question: "
            f"{effective_question}\n"
        )

        search_results = self._search_service.vector_search(
            query=effective_question,
            top_k=top_k
        )

        # TODO: temporarily adding for testing.
        for result in search_results:
            print(
                f"Score={result.similarity:.4f} | "
                f"Source={result.chunk.source_document} | "
                f"Chunk={result.chunk.chunk_index}"
            )

        relevant_results = [
            result
            for result in search_results
            if result.similarity >= self.MIN_SIMILARITY
        ]

        if not relevant_results:
            yield self.NO_CONTEXT_FOUND_MESSAGE
            return

        context = "\n\n".join(
            result.chunk.content
            for result in relevant_results
        )

        print("\n===== CONTEXT =====")
        print(context)
        print("===================\n")

        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        yield from self._llm_service.stream(prompt)
