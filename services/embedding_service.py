import ollama

class EmbeddingService:

    def __init__(self, model: str):
        self._model = model

    def embed(self, text: str):
        response = ollama.embeddings(
            model = self._model,
            prompt = text
        )
        return response["embedding"]