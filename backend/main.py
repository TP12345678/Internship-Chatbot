from config import DATA_FOLDER, GEMINI_API_KEY
from data_loader import load_documents_from_folder
from text_processor import chunk_text
from embedding_manager import EmbeddingManager
from vector_db_manager import VectorDBManager
from llm_manager import LLMManager

def main():
    print("Starting Chatbot Setup")

    # Initialize managers
    embedding_manager = EmbeddingManager()
    vector_db_manager = VectorDBManager()
    llm_manager = LLMManager()

    # Check if managers are properly initialized
    if not embedding_manager.get_model() or not vector_db_manager.collection or not llm_manager.model:
        print("One or more core components failed to initialize. Please check configurations and dependencies.")
        return

    # Step 1: Load and Extract Documents
    print("\n Loading and Extracting Documents")
    documents = load_documents_from_folder(DATA_FOLDER)
    if not documents:
        print("No documents found or extracted. Please ensure your 'data' folder contains supported files (PDF, PPTX, CSV, TXT).")
        print("Exiting.")
        return

    # Step 2: Chunk and Clean Text
    print("\nChunking and Cleaning Text")
    chunks = chunk_text(documents)
    if not chunks:
        print("No chunks created. This might indicate an issue with text extraction or cleaning.")
        print("Exiting.")
        return

    # Step 3: Create Embeddings
    print("\nCreating Embeddings")
    embeddings = embedding_manager.create_embeddings(chunks)
    if embeddings is None:
        print("Failed to create embeddings. Exiting.")
        return

    # Step 4: Add Documents to ChromaDB
    print("\nAdding Documents to ChromaDB")
    vector_db_manager.add_documents(embeddings, chunks)

    print("\nChatbot Setup Complete! You can now ask questions.")
    print("Type 'exit' to quit the chatbot.")

    # Step 5: Start Query Loop
    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() == 'exit':
            print("Goodbye!")
            break

        # Retrieve context from ChromaDB
        relevant_context = vector_db_manager.retrieve_context(user_query)

        if not relevant_context:
            print("No relevant information found in the knowledge base for your query.")
            continue

        # Generate response using Gemini
        response = llm_manager.generate_response(user_query, relevant_context)
        print("\nChatbot:", response)

if __name__ == "__main__":
    main()
