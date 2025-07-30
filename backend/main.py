from config import DATA_FOLDER, GEMINI_API_KEY # Assuming these are defined in config.py
from data_loader import load_documents_from_folder
from text_processor import chunk_text
from embedding_manager import EmbeddingManager
from vector_db_manager import VectorDBManager
from llm_manager import LLMManager
import os


_embedding_manager = None
_vector_db_manager = None
_llm_manager = None

_SINGLE_FILE_TO_DEBUG = None 
_FORCE_CHROMA_REINGESTION = False #new data

def _init_rag_chatbot_components():
    """
    Initializes the RAG chatbot components (EmbeddingManager, VectorDBManager, LLMManager),
    loads documents, creates chunks and embeddings, and adds them to ChromaDB.
    This function runs once when the main.py module is imported.
    """
    global _embedding_manager, _vector_db_manager, _llm_manager

    print("Initializing RAG Chatbot Components...")

    try:
        _embedding_manager = EmbeddingManager()
        _vector_db_manager = VectorDBManager()
        _llm_manager = LLMManager()

        if not _embedding_manager.get_model() or not _vector_db_manager.collection or not _llm_manager.model:
            print("ERROR: One or more core RAG components failed to initialize. Please check configurations and dependencies.")
            return

        print("Loading and Extracting Documents...")
        documents = load_documents_from_folder(DATA_FOLDER, single_file_path=_SINGLE_FILE_TO_DEBUG)

        if not documents:
            print("WARNING: No documents found or extracted. Chatbot will have limited knowledge.")
            return

        print("Chunking text...")
        chunks = chunk_text(documents)
        if not chunks:
            print("WARNING: No chunks created. This might indicate an issue with text extraction or cleaning. Chatbot will have limited knowledge.")
            return

        print("Creating embeddings...")
        embeddings = _embedding_manager.create_embeddings(chunks)
        if embeddings is None:
            print("ERROR: Failed to create embeddings. Chatbot will not function correctly.")
            return

        print("Adding documents to ChromaDB...")
        _vector_db_manager.add_documents(embeddings, chunks, force_reingestion=_FORCE_CHROMA_REINGESTION)
        print("RAG Chatbot components successfully initialized and knowledge base loaded.")

    except Exception as e:
        print(f"ERROR initialization: {e}")
        _embedding_manager = None
        _vector_db_manager = None
        _llm_manager = None


_init_rag_chatbot_components()

def ask_idc_chatbot(query: str) -> str:
    """
    Processes a user query using the RAG pipeline.
    This function is designed to be imported and called by app.py.
    """
    if not _vector_db_manager or not _llm_manager:
        print("ERROR: Chatbot core components not ready. Cannot process query.")
        return "I'm sorry, the chatbot is not fully initialized. Please try again later."

    try:
        relevant_context = _vector_db_manager.retrieve_context(query, n_results=5)
        response = _llm_manager.generate_response(query, relevant_context)
        return response
    except Exception as e:
        print(f"ERROR processing query in ask_idc_chatbot: {e}")
        return "I encountered an error while trying to answer your question. Please try again."

def main():
    """
    Main function for console-based chatbot interaction.
    This is the original entry point for running main.py directly.
    """
    if not _vector_db_manager or not _llm_manager:
        print("Chatbot components failed to initialize. Cannot run console mode.")
        return

    print("\nChatbot's ready (Console Mode).")
    print("Type 'exit' to quit the chatbot.")

    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() == 'exit':
            print("Exiting chatbot. Goodbye!")
            break

        response = ask_idc_chatbot(user_query)
        print("\nChatbot:", response)

if __name__ == "__main__":
    main()