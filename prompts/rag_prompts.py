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

QUERY_REWRITE_PROMPT = """
Given the conversation history and the latest user question,
rewrite the question so it is fully self-contained.

Only return the rewritten question.
Do not answer the question.

Conversation History:
{history}

Latest Question:
{question}

Rewritten Question:
"""
