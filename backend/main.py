from config import DATA_FOLDER, GEMINI_API_KEY
from data_loader import load_documents_from_folder
from text_processor import chunk_text
from embedding_manager import EmbeddingManager
from vector_db_manager import VectorDBManager
from llm_manager import LLMManager
import os 

def main():
    print("Chatbot Setup")

    SINGLE_FILE_TO_DEBUG = None #CHECK BEFORE RUNNING 
    
    FORCE_CHROMA_REINGESTION = False #CHECK BEFOR RUNNING 

    embedding_manager = EmbeddingManager()
    vector_db_manager = VectorDBManager()
    llm_manager = LLMManager()


    if not embedding_manager.get_model() or not vector_db_manager.collection or not llm_manager.model:
        print("One or more core components failed to initialize. Please check configurations and dependencies.")
        return

    
    print("\nLoading and Extracting Documents")
    
    
    documents = load_documents_from_folder(DATA_FOLDER, single_file_path=SINGLE_FILE_TO_DEBUG)
    
    if not documents:
        print("No documents found or extracted.")
        print("Exiting.")
        return


    print("\nchunking text")
    chunks = chunk_text(documents)
    if not chunks:
        print("No chunks created. This might indicate an issue with text extraction or cleaning.")
        print("Exiting.")
        return

    print("\ncreating embeddings")
    embeddings = embedding_manager.create_embeddings(chunks)
    if embeddings is None:
        print("Failed to create embeddings. Exiting.")
        return

    print("\nadding documents to chroma db")
    vector_db_manager.add_documents(embeddings, chunks, force_reingestion=FORCE_CHROMA_REINGESTION)

    print("\nchatbot's ready")
    print("Type 'exit' to quit the chatbot.")

    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() == 'exit':
            print("Exiting chatbot. Goodbye!")
            break

        relevant_context = vector_db_manager.retrieve_context(user_query, n_results=5)

        response = llm_manager.generate_response(user_query, relevant_context)
        print("\nChatbot:", response)

if __name__ == "__main__":
    main()
