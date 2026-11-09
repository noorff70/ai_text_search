from pydantic import BaseModel
from dataclasses import dataclass

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    # messages: list[Message]

class ChatResponse(BaseModel):
    response: str

class UserMessageRequest(BaseModel):
    message: str

@dataclass
class DocumentChunk:
    id: int | None
    source_document: str
    chunk_index: int
    content: str
    embedding: list[float]

@dataclass
class SearchResult:
    chunk: DocumentChunk
    similarity: float

@dataclass
class RagResponse:
    answer: str
    sources: list[str]
    chunk_count: int

