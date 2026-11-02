class RagService:

    def __init__(self, document_repository):
        self._repository = document_repository

    def retrieve(self, question: str):

        docs = self._repository.get_all_documents()
        
        print("\n=== ALL DOCS ===")
        for doc in docs:
            print(doc["name"])
        print("================\n")
        
        results = []
        words = question.lower().split()
        for doc in docs:
            score = 0
            text = doc["content"].lower()

            for word in words:
                if word in text:
                    score += 1

            results.append(
                {
                    "content": doc["content"],
                    "score": score
                }
            )

        results = [
            r for r in results
            if r["score"] > 0
        ]

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:3]