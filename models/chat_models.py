from pydantic import BaseModel

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

