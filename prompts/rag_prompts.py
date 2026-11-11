RAG_PROMPT = """
You are a helpful assistant.

Use only the provided context to answer the question.

If the answer cannot be found in the context,
say:
"I could not find relevant information in the knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""
