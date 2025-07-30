import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")

CHROMA_DB_PATH = "./chroma_db"

COLLECTION_NAME = "company_data_collection"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

GEMINI_MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Created data folder: {DATA_FOLDER}")

if not os.path.exists(CHROMA_DB_PATH):
    os.makedirs(CHROMA_DB_PATH)
    print(f"Created ChromaDB folder: {CHROMA_DB_PATH}")
