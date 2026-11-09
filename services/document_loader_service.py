# services/document_loader_service.py

from repositories.document_repository import DocumentRepository
from repositories.vector_repository import VectorRepository
from services.embedding_service import EmbeddingService
from models.chat_models import DocumentChunk
from utilities.text_chunker import chunk_text


class DocumentLoaderService:

    def __init__(
        self,
        document_repository: DocumentRepository,
        vector_repository: VectorRepository,
        embedding_service: EmbeddingService
    ):
        self._document_repository = document_repository
        self._vector_repository = vector_repository
        self._embedding_service = embedding_service

    def load_documents(self):

        documents = (
            self._document_repository.get_all_documents()
        )

        for document in documents:

            chunks = chunk_text(
                document["content"]
            )

            for chunk_index, chunk in enumerate(chunks):

                embedding = ( self._embedding_service.embed(chunk))

                self._vector_repository.save_chunk(
                    DocumentChunk(
                        id=None,
                        source_document=document["name"],
                        chunk_index=chunk_index,
                        content=chunk,
                        embedding=embedding
                    )
                )