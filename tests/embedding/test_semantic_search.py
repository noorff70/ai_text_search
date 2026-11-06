from services.embedding_service import EmbeddingService
from utilities.vector_utils import cosine_similarity

embedding_service = EmbeddingService(
    "nomic-embed-text"
)

with open("data/documents/fastapi.txt", "r") as f:
    fastapi_text = f.read()

with open("data/documents/python.txt", "r") as f:
    python_text = f.read()

fastapi_embedding = embedding_service.embed(
    fastapi_text
)

python_embedding = embedding_service.embed(
    python_text
)

question = "How do I create a REST API?"

question_embedding = embedding_service.embed(
    question
)

fastapi_score = cosine_similarity(
    question_embedding,
    fastapi_embedding
)

python_score = cosine_similarity(
    question_embedding,
    python_embedding
)

documents = [
    {
        "name": "FastAPI",
        "text": fastapi_text,
        "embedding": fastapi_embedding
    },
    {
        "name": "Python",
        "text": python_text,
        "embedding": python_embedding
    }
]
best_document = None
best_score = -1

for document in documents:

    score = cosine_similarity(
        question_embedding,
        document["embedding"]
    )

    if score > best_score:
        best_score = score
        best_document = document

print(f"Winner: {best_document['name']}")
print(f"Score: {best_score}")

# print(f"FastAPI: {fastapi_score}")
# print(f"Python: {python_score}")