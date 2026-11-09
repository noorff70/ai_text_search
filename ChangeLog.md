[v0.1] - Foundation
Added
FastAPI application structure
Repository layer
Service layer
SQLite database access
Dependency injection patterns
Initial Ollama integration
Test project structure
Notes
Project scaffolding and architecture established.

==============================

[v0.2] - Vector Search
Added
SQLite-based vector storage
Document chunk storage
Embedding generation using Ollama (nomic-embed-text)
Similarity search service
Document ingestion pipeline
Verified
Successfully stored document chunks
Successfully generated embeddings
Successfully retrieved relevant chunks based on semantic similarity
Notes
First successful semantic search implementation.

=============================
[v0.3] - Conversational RAG
Added
Conversation history support
Context-aware question rewriting
Follow-up question handling
Retrieval-Augmented Generation (RAG) response flow
Prompt guardrails to prevent hallucinations
Verified
"What is FastAPI?" style questions
Follow-up questions using pronouns:
"What is it used for?"
"Who created it?"
"What documentation does it provide?"
"What validation library does it use?"
Fixed
Recreated vector database to eliminate stale data and duplicate retrieval results
Retrieval now returns correct context for conversational questions
Notes
First end-to-end conversational RAG prototype working successfully.