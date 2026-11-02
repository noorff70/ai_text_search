from pathlib import Path

class DocumentRepository:

    def __init__(self, document_folder = "data/documents"):
        self._folder = document_folder

    def get_all_documents(self):
        docs = []
        for file in Path(self._folder).glob("*.txt"):
            docs.append({
                "name": file.name,
                "content": file.read_text(encoding="utf-8")
            })
        return docs   