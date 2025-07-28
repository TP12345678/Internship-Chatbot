from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL_NAME

class VectorDBManager:
    """Manages interactions with ChromaDB."""
    def __init__(self):
        self.client = PersistentClient(path=CHROMA_DB_PATH)
        # Define the embedding function for ChromaDB to ensure consistency
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self):
        """Gets or creates the ChromaDB collection."""
        try:
            collection = self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                embedding_function=self.embedding_function
            )
            print(f"ChromaDB collection '{COLLECTION_NAME}' ready. Contains {collection.count()} documents.")
            return collection
        except Exception as e:
            print(f"Error getting/creating ChromaDB collection: {e}")
            return None

    def add_documents(self, embeddings, chunks):
        """Adds documents (chunks and their embeddings) to the ChromaDB collection."""
        if not self.collection:
            print("ChromaDB collection not initialized. Cannot add documents.")
            return

        if self.collection.count() > 0:
            print(f"ChromaDB collection '{COLLECTION_NAME}' already contains {self.collection.count()} documents. Skipping re-ingestion.")
            return

        ids = [chunk["id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"source": chunk["source"]} for chunk in chunks]

        try:
            print(f"Adding {len(ids)} documents to ChromaDB collection '{COLLECTION_NAME}'...")
            self.collection.add(
                embeddings=embeddings.tolist(), # Convert numpy array to list
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print("Documents added to ChromaDB.")
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")

    def retrieve_context(self, query, n_results=3):
        """
        Retrieves relevant document chunks from ChromaDB based on the query.
        Returns a list of relevant text snippets.
        """
        if not self.collection:
            print("ChromaDB collection not initialized. Cannot retrieve context.")
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=['documents', 'metadatas']
            )
            context = []
            if results and results['documents']:
                for i, doc_text in enumerate(results['documents'][0]):
                    source = results['metadatas'][0][i]['source']
                    context.append(f"Source: {source}\nContent: {doc_text}")
            return context
        except Exception as e:
            print(f"Error retrieving context from ChromaDB: {e}")
            return []
