from services.embedding_service import EmbeddingService

embedding_service = EmbeddingService("nomic-embed-text")

vector = embedding_service.embed("What is FastAPI?")

print(type(vector))
print(len(vector))
print(vector[:5])