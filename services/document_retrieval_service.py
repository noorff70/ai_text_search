from pathlib import Path

from services.embedding_service import EmbeddingService
from utilities.vector_utils import cosine_similarity


class DocumentRetrievalService:

    def __init__(self, embedding_service: EmbeddingService):
        self._embedding_service = embedding_service
        self._documents = []

        self._load_documents()

    def _load_documents(self):
        document_folder = Path("data/documents")

        for file_path in document_folder.glob("*.txt"):

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            embedding = self._embedding_service.embed(text)

            self._documents.append({
                "name": file_path.stem,
                "text": text,
                "embedding": embedding
            })

    def get_best_document(self, question: str):

        question_embedding = self._embedding_service.embed(
            question
        )

        best_document = None
        best_score = -1

        for document in self._documents:

            score = cosine_similarity(
                question_embedding,
                document["embedding"]
            )

            if score > best_score:
                best_score = score
                best_document = document

        return best_document

    def get_best_document_with_score(self, question: str):

        question_embedding = self._embedding_service.embed(
            question
        )

        best_document = None
        best_score = -1

        for document in self._documents:

            score = cosine_similarity(
                question_embedding,
                document["embedding"]
            )

            if score > best_score:
                best_score = score
                best_document = document

        return {
            "document": best_document,
            "score": best_score
        }