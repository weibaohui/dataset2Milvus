from sentence_transformers import SentenceTransformer


class Transformer:

    def __init__(self):
        self.SentenceTransformerName = "thenlper/gte-large"
        self.embedding_model = SentenceTransformer(self.SentenceTransformerName)

    def get_embedding(self, text: str) -> list[float]:
        text = f"{text}"
        if not text.strip():
            print("Attempted to get embedding for empty text.")
            return []

        embedding = self.embedding_model.encode(text)

        return embedding.tolist()
