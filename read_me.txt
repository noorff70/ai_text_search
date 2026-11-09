-------------------------Day 1 ------------------------------------------------
Create folder
python -m venv venv
.\venv\Scripts\activate

docker run -d -v ollama_data:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull llama3.2
docker volume inspect ollama_data (for inspecting folder)
pip install ollama
pip install fastapi uvicorn ollama
================
Running and testing ollama
Test if docker ollama is running, run in PS:
Invoke-RestMethod `
  -Uri "http://localhost:11434/api/tags"
  
or: curl http://localhost:11434/api/tags

pull and verify model
ollama pull llama3.2
docker exec -it ollama ollama list

run a test prompt
docker exec -it ollama ollama run llama3.2
What is FastAPI?

Testing
uvicorn main:app --reload
http://localhost:8000/docs
{
  "message": "What is FastAPI?"
}


==========

Your FastAPI App
        │
        ▼
Python ollama package
        │
        ▼
Ollama Server (localhost:11434)
        │
        ▼
Llama 3.2 Model

===== Milestone 2==================== Conversation memory
a. added a list as request. Previously it was one string only. List makes it conversational.
JSON to run:
{
    "messages": [
        {
            "role": "user",
            "content": "What is FastAPI?"
        },
        {
            "role": "assistant",
            "content": "FastAPI is a web framework."
        },
        {
            "role": "user",
            "content": "Who created it?"
        }
    ]
}

==============Milestone 3 ======================= Add Db and test
Created a db script (create_db.py)
Created a repositoty repositories/conversation_repositoty.py

services/
├── ollama_service.py
└── chat_service.py

ChatService
    ↓
ConversationRepository
    ↓
OllamaService

POST /conversations
            ↓
ConversationRepository
            ↓
SQLite

POST /conversations/{id}/chat
            ↓
ChatService
            ↓
ConversationRepository
            ↓
OllamaService
            ↓
Ollama


User sends message
    ↓
Save user message
    ↓
Load conversation history
    ↓
Send history to Ollama
    ↓
Save assistant response
    ↓
Return assistant response


python -m tests.ConversationRepository_test

Swagger testing:
A. /conversations
Response:
{
    "conversation_id": 1
}
B. Send message:
/ conversations/1/chat
Body:
{
    "message": "What is FastAPI?"
}
Response:
{
    "response": "FastAPI is a modern Python web framework..."
}
C. send another message:
/conversations/1/chat
{
    "message": "Who created it?"
}
Because the ChatService loads all previous messages from SQLite before calling Ollama, the model will know that "it" = FastAPI.

retrieve conversation:
GET /conversations/{conversation_id}

==============Streaming Chat response:
Learning objectives:
-FastAPI StreamingResponse
-generators (yield)
-Ollama streaming
-real-world AI chat architecture

API- @app.post("/chat/stream") -- this is without conversation_id
{
  "messages": [
    {
      "role": "user",
      "content": "Tell me about FastAPI"
    }
  ]
}

Test from PS:
$body = @{
    messages = @(
        @{
            role = "user"
            content = "Tell me about FastAPI"
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod `
    -Uri "http://localhost:8000/chat/stream" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
	
	Honestly, based on what you've shown, I'd say we've successfully proven the streaming part. The next thing I would do is wire the endpoint through ChatService.stream_chat() so that conversation history stored in SQLite participates in the prompt and the generated response gets saved back to the database. That's the natural next step in your architecture.

Now hook this new API as follows:
API
 ↓
ChatService
 ↓
ConversationRepository
 ↓
OllamaService
 ↓
Ollama

How the yield is working:
Ollama
  ↓
yield chunk
  ↓
OllamaService.stream()
  ↓
yield chunk
  ↓
ChatService.stream_chat()
  ↓
yield chunk
  ↓
StreamingResponse

both yields are needed in your current design. The first yield streams data from Ollama. The second yield forwards that data to FastAPI while allowing ChatService to accumulate and save the final response in the database. This is actually the cleanest design for the architecture you're building.

new JSON:
{
  "conversation_id": 2,
  "message": "Tell me about FastAPI"
}

=========================RAG implementation

Current flow:
User
  ↓
FastAPI
  ↓
Ollama
  ↓
Answer
-----
RAG flow:
User
  ↓
FastAPI
  ↓
Vector Search
  ↓
Relevant Documents
  ↓
Ollama
  ↓
Answer using documents

Dependency graph:
chat endpoint
    │
    ▼
get_chat_service()
    │
    ├── get_repository()
    │
    ├── get_ollama_service()
    │
    └── get_rag_service()
            │
            ▼
    get_document_repository()
	
==========================
Populate fastapi.txt and python.txt
Test /chat_with_rag
Verify retrieved documents
Discuss chunking
Add embeddings
Introduce ChromaDB
===============================
Test following API:
http://localhost:8000/docs#/default/chat_with_rag_chat_with_rag_post

{
  "conversation_id": "1",
  "message": "What is the name of the secret FastAPI mascot?"
}

===================================================
embedding:
docker exec -it ollama ollama pull nomic-embed-text

FastAPI
   ↓
Chat API
   ↓
ChatService
   ↓
EmbeddingService
   ↓
Local Vector Store (memory)
--------------
User Question
      ↓
EmbeddingService
      ↓
Find Relevant Chunks
      ↓
OllamaService
      ↓
Generate Final Answer
------------------------
We have created vector_utils.py and embedding_service.py

The next step is 
Question
   ↓
Question Embedding
   ↓
Compare With Document Embeddings
   ↓
Choose Best Document

Now create a semantic_search_text.py that will do some semantic test as follows:
Read fastapi.txt -> Read python.txt -> Generate embeddings for both -> Generate an embedding for a question -> ->Calculate cosine similarity -> Print scores

and do the test:
PS D:\dev\python_projects\ai_1> python -m tests.embedding.semantic_search_test

We have done so far:
✅ Chat endpoint
✅ Ollama integration
✅ Basic RAG
✅ Document loading
✅ EmbeddingService
✅ Vector generation
✅ Cosine similarity
✅ Semantic search test

And the next milestone:
Semantic search test
        ↓
Retrieve winning document
        ↓
Move retrieval logic into ChatService
        ↓
Replace keyword search

We changed the test so that we can return the best document as follows:
Question -> Embedding -> Find Best Document -> Return Document Content

------
Now we are doing chunking, and the flow is:
Document -> Chunks-> Embeddings -> Vector Store -> Similarity Search -> Top 3 Chunks -> Ollama

Currently we are doing as follows:
Question -> Generate embedding -> Compare against documents

Next objective:
Documents -> Chunk -> Embed once -> Store vectors in SQLite -> Query embedding -> Similarity search

------------
So far completed:
 ✅ Ollama installed and running
 ✅ nomic-embed-text working
 ✅ Embedding service created
 ✅ Cosine similarity implemented
 ✅ Document chunking implemented
 ✅ SQLite vector table created
 ✅ Chunks stored with embeddings
 ✅ Verified data is being persisted
 
 fastapi.txt
    ↓
Chunking
    ↓
Embeddings (Ollama)
    ↓
SQLite

Continue my Ollama RAG project

====================================

Responsibilities:
EmbeddingService
    Generates embeddings
    Computes similarity

VectorRepository
    Saves chunks
    Loads chunks

VectorSearchService
    Orchestrates search
	
Created a test:
(venv) PS D:\dev\python_projects\ai_1> python -m tests.services.test_vector_search_service

Now test this: (End-toEnd Test)
python -m tests.services.test_vector_rag_service
This test provided the following:
Document
    ↓
Chunking
    ↓
Embeddings
    ↓
SQLite
    ↓
Vector Search
    ↓
Context Assembly
    ↓
llama3.2
    ↓
Answer

Current Project Status

Completed

Ollama setup
Embedding service
Chunking
SQLite vector storage
Cosine similarity
Vector repository
Vector search service
LLM service
Vector RAG service
End-to-end testing

Remaining

Better prompts
RagResponse model
Source citations
Retrieval debugging/logging
FastAPI /ask endpoint
Conversation history (optional)
Metadata filtering (optional)
Streaming responses (optional)

===========================================
The typical flow is this:
Document
   ↓
load_document()
   ↓
chunk_document()
   ↓
generate_embeddings()
   ↓
SAVE chunks + embeddings to SQLite
   ↓
----------------------------------
Later...
----------------------------------
User Question
   ↓
VectorSearchService
   ↓
Load saved chunks + embeddings
   ↓
Similarity Search
   ↓
Return matching chunks
   ↓
VectorRAGService
   ↓
Build prompt
   ↓
Ollama
   ↓
Answer

There are two flows:
Flow 1: Ingestion Pipeline (runs once per document)

This is the pipeline that populates the database.

Plain Text
PDF/TXT
↓
load_document()
↓
chunk_document()
↓
EmbeddingService.embed(chunk)
↓
VectorRepository.save_chunk()
↓
document_chunks table

Flow 2: Query Pipeline (runs for every user question)

Your vector_search_service.py belongs entirely to this flow.

Plain Text
Question
↓
EmbeddingService.embed(question)
↓
VectorRepository.get_all_chunks()
↓
cosine_similarity()
↓
Top K Results

Flow 3: RAG Pipeline

Your VectorRagService sits on top of the search layer.

Plain Text
Question
↓
VectorSearchService
↓
Top K Chunks
↓
Build Context
↓
LlmService
↓
Answer

Honestly, this looks much cleaner than many beginner RAG implementations because you have kept:

persistence isolated in the repository
search isolated in its own service
prompt generation isolated in the RAG service
model calls isolated behind services

That's very close to the same separation you'd see in a production application.

This is dependency injection
ChatService
├── OllamaService
├── RagService
└── VectorRagService
    ├── VectorSearchService
    │   ├── EmbeddingService
    │   └── VectorRepository
    └── LlmService

Here is more explanation:
Flow 2 = Retrieval Layer (Search Engine)

This part answers:

"Which chunks are relevant to the question?"

Plain Text
Question
↓
EmbeddingService.embed(question)
↓
VectorRepository.get_all_chunks()
↓
cosine_similarity()
↓
Top K Results

The output is:

Python
[
Chunk("FastAPI is a modern web framework..."),
Chunk("Dependency injection allows..."),
Chunk("ASGI is the interface...")
]

No LLM is involved yet.

This layer is useful by itself because you can:

Test retrieval quality
Verify embeddings work correctly
Debug chunk ranking
Build document search applications
Reuse retrieval for multiple AI features
Flow 3 = Answer Generation Layer (RAG)

This part answers:

"Using the retrieved chunks, generate an answer."

Plain Text
Question
↓
VectorSearchService
↓
Top K Chunks
↓
Build Context
↓
LlmService
↓
Answer

The output becomes:

Plain Text
FastAPI is a modern Python web framework designed
for building APIs quickly. It is based on ASGI and
provides automatic validation through Pydantic.

Now the LLM is involved.

Why Not Skip Flow 2?

Because the LLM needs context.

Suppose the user asks:

Plain Text
What fruit types exist in my database?

Without retrieval:

Plain Text
Question
↓
LlmService
↓
Hallucinated answer

The LLM has no idea what's in your SQLite database.

With retrieval:

Plain Text
Question
↓
VectorSearchService
↓
Chunks about fruits
↓
LlmService
↓
Accurate answer

The search layer fetches relevant data; the LLM only summarizes and reasons over it.

Architecture View

A cleaner representation is:

Plain Text
┌───────────────────┐
│ VectorRepository │
└─────────┬─────────┘
│
┌─────────▼─────────┐
│VectorSearchService│
└─────────┬─────────┘
│
Top K Chunks
│
┌─────────▼─────────┐
│ VectorRagService │
└─────────┬─────────┘
│
┌─────────▼─────────┐
│ LlmService │
└─────────┬─────────┘
│
Answer

So:

VectorSearchService = retrieval only
VectorRagService = retrieval + answer generation
LlmService = text generation only
Why This Separation Is Good Design

Imagine later you want:

Feature 1: Document Search
Plain Text
User Question
↓
VectorSearchService
↓
Show matching chunks

No LLM needed.

Feature 2: Citations
Plain Text
User Question
↓
VectorSearchService
↓
Show top chunks with scores

No LLM needed.

Feature 3: RAG Chat
Plain Text
User Question
↓
VectorRagService
↓
LLM Answer

Uses the same retrieval component.

This follows the Single Responsibility Principle:

VectorSearchService → find relevant chunks
VectorRagService → orchestrate RAG
LlmService → talk to Ollama

In your Ollama project specifically, you're at the stage where you're building Flow 2 first because if retrieval isn't working correctly, the RAG layer will produce poor answers regardless of how good the LLM is. The usual progression is:

Plain Text

===============================

Things we want to do now:
1. Similarity threshold
2. "No relevant context found" handling
3. Source citations
4. Multi-document testing
5. Chat history aware Vector RAG

What you've accomplished

Your RAG system now has:

✅ Embedding generation
 ✅ Document chunking
 ✅ SQLite vector storage
 ✅ Cosine similarity search
 ✅ Top-K retrieval
 ✅ Similarity scoring
 ✅ Similarity threshold filtering
 ✅ Hallucination reduction
 ✅ No-context detection
 ✅ Retrieval diagnostics

This is already a respectable RAG implementation.

We need to implement like this:
✅ Ingestion
✅ Chunking
✅ Embeddings
✅ SQLite storage
✅ Retrieval
✅ Citation support
⬜ Prompt templates
⬜ Conversation memory
⬜ Hybrid search (BM25 + vectors)
⬜ Reranking
⬜ Evaluation dataset
⬜ Streaming responses