import ollama

# This is for vector search
class LlmService:

    def __init__(self, model: str):
        self._model = model

    def generate(self, prompt: str):

        response = ollama.chat(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]