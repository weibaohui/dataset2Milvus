import os

from sentence_transformers import SentenceTransformer


class Transformer:

    def __init__(self):
        if os.getenv('TRANSFORMERS_OFFLINE') == '1':
            self.SentenceTransformerName = os.getenv('TRANSFORMERS_OFFLINE_NAME')
            self.embedding_model = SentenceTransformer(os.getenv('TRANSFORMERS_OFFLINE_PATH'))
        else:
            self.SentenceTransformerName = "thenlper/gte-large-zh"
            self.embedding_model = SentenceTransformer(self.SentenceTransformerName)

    def get_embedding(self, text: str) -> list[float]:
        text = f"{text}"
        if not text.strip():
            print("Attempted to get embedding for empty text.")
            return []

        embedding = self.embedding_model.encode(text)

        return embedding.tolist()
