from repositories.document_repository import DocumentRepository
from services.rag_service import RagService

def test_retrieve_fastapi():
    repo = DocumentRepository()
    rag = RagService(repo)

    results = rag.retrieve("Who created FastAPI?")
    assert len(results) > 0

def test_retrieved_documents_have_score():

    repo = DocumentRepository()
    rag = RagService(repo)
    results = rag.retrieve(
        "Who created FastAPI?"
    )
    assert results[0]["score"] > 0
