from repositories.conversation_repository import ConversationRepository
from services.ollama_service import OllamaService
from services.rag_service import RagService
from services.vector_rag_service import VectorRagService


class ChatService:
    def __init__(self, repository: ConversationRepository, 
                 ollama_service: OllamaService, 
                 rag_service: RagService,
                 vector_rag_service: VectorRagService):
        self._repository = repository
        self._ollama_service = ollama_service
        self._rag_service = rag_service
        self._vector_rag_service = vector_rag_service

    def chat (self, conversation_id: int, user_message:str)-> str:
        
        # save message
        self._repository.add_message(conversation_id, "user", user_message)
        
        # load full conversation
        messages = self._repository.get_messages(conversation_id)
        
        # send to ollama
        answer = self._ollama_service.ask(messages)

        # save AI response
        self._repository.add_message( conversation_id, "assistant", answer )

        return answer


        # This creates a generator that produces pieces of the response as Ollama generates them.
    # def stream(self, messages: list[dict]):
    #     stream = ollama.chat(
    #         model = self.__model,
    #         messages = messages,
    #         stream = True
    #     )
    #     for chunk in stream:
    #         yield chunk.message.content


    def stream_chat(self, conversation_id: int, user_message: str):
   
        self._repository.add_message(conversation_id, "user", user_message)

        messages = self._repository.get_messages(conversation_id )

        # print("Messages sent to Ollama:")
        # for m in messages:
        #     print(m)

        full_answer = ""
        for chunk in self._ollama_service.stream(messages):
            full_answer += chunk
            yield chunk

        self._repository.add_message(conversation_id, "assistant", full_answer )


    # This calls rag service
    def ask (self, question: str):
        contexts = self._rag_service.retrieve(question)
        
        print("\n==== RETRIEVED ====")
        for doc in contexts:
            print(doc["content"])
        print("===================\n")
        
        
        context_text = "\n\n".join(
            c["content"]
            for c in contexts
        )
        prompt = f"""
CONTEXT:

{context_text}

QUESTION:

{question}

ANSWER:
"""

        print("\n===== PROMPT =====")
        print(prompt)
        print("==================\n")
 
        return self._ollama_service.ask(
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    # This asks vector rag service
    def ask_vector(self, question: str):
            return self._vector_rag_service.ask(
                question
            )