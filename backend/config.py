import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- General Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Reads from .env

# Folder where your company's data files (PDF, PPTX, CSV, TXT) are stored
DATA_FOLDER = "./data"

# Path to store ChromaDB persistent data
CHROMA_DB_PATH = "./chroma_db"

# Name of the collection in ChromaDB where document chunks will be stored
COLLECTION_NAME = "company_data_collection"

# --- Model Configuration ---
# Embedding model for document embeddings (Sentence-Transformers)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

# Gemini model for RAG response generation
GEMINI_MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"

# --- Text Processing Configuration ---
# Max characters per chunk for text splitting
CHUNK_SIZE = 1000
# Overlap between chunks to maintain context
CHUNK_OVERLAP = 200

# Ensure data folder exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Created data folder: {DATA_FOLDER}")

# Ensure ChromaDB path exists
if not os.path.exists(CHROMA_DB_PATH):
    os.makedirs(CHROMA_DB_PATH)
    print(f"Created ChromaDB folder: {CHROMA_DB_PATH}")
