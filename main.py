from fastapi import FastAPI, Depends

from models.chat_models import ChatRequest, ChatResponse, UserMessageRequest
from repositories.conversation_repository import ConversationRepository
from repositories.document_repository import DocumentRepository
from services.chat_service import ChatService
from services.ollama_service import OllamaService
from fastapi.responses import StreamingResponse

from services.rag_service import RagService

# from repositories.conversation_repository import (
#     ConversationRepository
# )

app = FastAPI()

def get_repository():
    return ConversationRepository(
        "data/chatbot.db"
    )

def get_ollama_service():
    return OllamaService("llama3.2")

def get_document_repository():
    return DocumentRepository()

def get_rag_service( document_repository: DocumentRepository = Depends(get_document_repository)):
    return RagService(document_repository)


def get_chat_service(repository : ConversationRepository = Depends(get_repository), ollama_service : OllamaService = Depends(get_ollama_service), rag_service: RagService= Depends(get_rag_service)):

     
    return ChatService(
        repository = repository,
        ollama_service = ollama_service,
        rag_service = rag_service
    )

@app.post ("/chat_with_ollama_directly", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest,  chat_service: ChatService = Depends(get_chat_service)):
    response = chat_service.chat(
        request.conversation_id,
        request.message
    )
    return ChatResponse(
        answer = response
    )

@app.post("/chat_with_rag")
def chat_with_rag(request: ChatRequest, service: ChatService= Depends(get_chat_service)):
    answer = service.ask(request.message)
    return {"answer": answer}


@app.post("/conversations")
def create_conversation( repository: ConversationRepository = Depends( get_repository)):
    conversation_id = repository.create_conversation()

    return {
        "conversation_id": conversation_id
    }

@app.post( "/conversations/{conversation_id}/chat", response_model=ChatResponse)
def chat(
    conversation_id: int, request: UserMessageRequest, chat_service: ChatService = Depends( get_chat_service)):
    answer = chat_service.chat( conversation_id, request.message )

    return ChatResponse(
        response=answer
    )

@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id:int, repository: ConversationRepository = Depends(get_repository)):
    messages = repository.get_messages(conversation_id)

    return {
        "conversation_id": conversation_id,
        "messages": messages
    }

@app.get("/messages")
def get_all_messages(repository: ConversationRepository= Depends(get_repository)):
    messages = repository.get_all_msgs()
    return messages

# DELETE /conversations/{conversation_id}

# This is to call ollama_service directly. But actually we need to modify this to go through chat_service
# @app.post("/chat/stream")
# def stream_chat(request: ChatRequest, ollama_service = Depends(get_ollama_service)):
#     return StreamingResponse(
#         ollama_service.stream(request.messages),
#         media_type="text/plain"
#     )

#New api to hook with chat service?
@app.post( "/chat/stream")
def stream_chat(request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)):
    
    return StreamingResponse(
        chat_service.stream_chat(
            request.conversation_id,
            request.message
        ),
        media_type="text/event-stream"
    )