from ollama import Client

client = Client(host="http://localhost:11434")

response = client.embed(
    model="nomic-embed-text",
    input="FastAPI is a Python web framework"
)

embedding = response["embeddings"][0]

print(f"Length: {len(embedding)}")
print(embedding[:5])