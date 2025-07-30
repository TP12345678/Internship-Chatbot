from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME

class EmbeddingManager:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            print(f"Loaded embedding model: {EMBEDDING_MODEL_NAME}")
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            print("Please ensure you have an active internet connection or the model is cached locally.")
            self.model = None 

    def get_model(self):
        return self.model

    def create_embeddings(self, chunks):
        if not self.model:
            print("Embedding model not loaded. Cannot create embeddings.")
            return None

        texts = [chunk["text"] for chunk in chunks]
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print("Embeddings generated.")
        return embeddings
