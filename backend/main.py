# main.py


from config import DATA_FOLDER, GEMINI_API_KEY
from data_loader import load_documents_from_folder
from text_processor import chunk_text
from embedding_manager import EmbeddingManager
from vector_db_manager import VectorDBManager
from llm_manager import LLMManager
import os # Import os for path handling

def main():
    print("--- Starting Chatbot Setup ---")

    # --- Production Settings ---
    # Set to None to process all files in DATA_FOLDER.
    # For debugging a single file, set its path here (e.g., "./data/your_file.txt")
    SINGLE_FILE_TO_DEBUG = None # <--- Set to None for normal operation
    
    # Set to True if you have added/modified data in the 'data' folder
    # and want to force ChromaDB to re-ingest everything.
    # Set to False for faster subsequent runs if data hasn't changed.
    FORCE_CHROMA_REINGESTION = False # <--- Set to False for normal operation
    # ---------------------------

    # Initialize managers
    embedding_manager = EmbeddingManager()
    vector_db_manager = VectorDBManager()
    llm_manager = LLMManager()

    # Check if managers are properly initialized
    if not embedding_manager.get_model() or not vector_db_manager.collection or not llm_manager.model:
        print("One or more core components failed to initialize. Please check configurations and dependencies.")
        return

    # Step 1: Load and Extract Documents
    print("\n--- Step 1: Loading and Extracting Documents ---")
    
    # Pass single_file_path to load_documents_from_folder
    documents = load_documents_from_folder(DATA_FOLDER, single_file_path=SINGLE_FILE_TO_DEBUG)
    
    if not documents:
        print("No documents found or extracted. Please ensure your 'data' folder contains supported files (PDF, PPTX, CSV, TXT, common images).")
        print("Exiting.")
        return

    # Step 2: Chunk and Clean Text
    print("\n--- Step 2: Chunking and Cleaning Text ---")
    chunks = chunk_text(documents)
    if not chunks:
        print("No chunks created. This might indicate an issue with text extraction or cleaning.")
        print("Exiting.")
        return

    # --- Removed: DEBUGGING OUTPUT: Print all chunks ---
    # This section is removed for production use.
    # If you need to debug chunks again, temporarily uncomment this block.
    # print("\n--- ALL GENERATED CHUNKS (from file(s)) ---")
    # for i, chunk in enumerate(chunks):
    #     print(f"Chunk {i+1} (Source: {chunk['source']}):")
    #     print(f"ID: {chunk['id']}")
    #     print("Content:")
    #     print(f"{chunk['text']}")
    #     print("---")
    # print("-------------------------------------------\n")


    # Step 3: Create Embeddings
    print("\n--- Step 3: Creating Embeddings ---")
    embeddings = embedding_manager.create_embeddings(chunks)
    if embeddings is None:
        print("Failed to create embeddings. Exiting.")
        return

    # Step 4: Add Documents to ChromaDB
    print("\n--- Step 4: Adding Documents to ChromaDB ---")
    vector_db_manager.add_documents(embeddings, chunks, force_reingestion=FORCE_CHROMA_REINGESTION)

    print("\n--- Chatbot Setup Complete! You can now ask questions. ---")
    print("Type 'exit' to quit the chatbot.")

    # Step 5: Start Query Loop
    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() == 'exit':
            print("Exiting chatbot. Goodbye!")
            break

        # Retrieve context from ChromaDB
        relevant_context = vector_db_manager.retrieve_context(user_query, n_results=5)

        # --- Removed: DEBUGGING OUTPUT: Print Retrieved Context ---
        # This section is removed for production use.
        # If you need to debug retrieved context again, temporarily uncomment this block.
        # print("\n--- Retrieved Context for current query ---")
        # if relevant_context:
        #     for i, item in enumerate(relevant_context):
        #         print(f"Context {i+1}:\n{item}\n---")
        # else:
        #     print("No relevant context found in ChromaDB for this query.")
        # print("-------------------------------------------\n")

        # Generate response using Gemini
        response = llm_manager.generate_response(user_query, relevant_context)
        print("\nChatbot:", response)

if __name__ == "__main__":
    main()
