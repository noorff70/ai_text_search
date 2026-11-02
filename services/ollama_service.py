from ollama import chat
import ollama

class OllamaService:

    def __init__(self, model: str):
        self.__model = model

    def ask(self, messages):
        response = chat(
            model= self.__model,
            messages= messages
        )
        return response.message.content

    def stream(self, messages):
        stream = ollama.chat(
            model=self.__model,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            content = chunk["message"]["content"]
            # print(f"Chunk: [{content}]")
            yield content