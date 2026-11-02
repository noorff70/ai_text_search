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
Project Architecture
FastAPI
    ↓
Chat API
    ↓
Ollama (Llama 3.2)
    ↓
SQLite Conversation Memory
    ↓
RAG Knowledge Base
    ↓
Web UI

============
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


