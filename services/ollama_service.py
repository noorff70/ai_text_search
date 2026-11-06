from ollama import chat
import ollama

class OllamaService:

    def __init__(self, model: str):
        self._model = model

    def ask(self, messages):
        response = chat(
            model= self._model,
            messages= messages
        )
        return response.message.content

    def stream(self, messages):
        stream = ollama.chat(
            model=self._model,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            content = chunk["message"]["content"]
            # print(f"Chunk: [{content}]")
            yield content