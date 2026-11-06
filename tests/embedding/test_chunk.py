from utilities.text_chunker import chunk_text

text = """
FastAPI is a modern web framework.

FastAPI was created by Sebastián Ramírez.

FastAPI automatically generates OpenAPI documentation.

The secret FastAPI mascot is Bob.
"""

chunks = chunk_text(text, 50)

for i, chunk in enumerate(chunks):
    print()
    print(f"Chunk {i + 1}")
    print(chunk)
