from repositories.document_repository import DocumentRepository

def test_get_all_documents():
    repo = DocumentRepository()
    docs = repo.get_all_documents()
    assert len(docs) >0

def test_document_has_name_and_content():
    repo = DocumentRepository()
    docs = repo.get_all_documents()
    doc = docs[0]
    assert "name" in doc
    assert "content" in doc
