from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(documents):
    """
    Chunks the extracted text documents into smaller, manageable pieces.
    Returns a list of dictionaries, each containing 'chunk_id', 'text', and 'source'.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = []
    chunk_id_counter = 0
    for doc in documents:
        # Simple cleaning: remove excessive whitespace
        cleaned_text = " ".join(doc["text"].split()).strip()
        if not cleaned_text:
            continue

        doc_chunks = text_splitter.split_text(cleaned_text)
        for i, chunk_text in enumerate(doc_chunks):
            chunks.append({
                "id": f"chunk_{chunk_id_counter}",
                "text": chunk_text,
                "source": doc["source"]
            })
            chunk_id_counter += 1
    print(f"Created {len(chunks)} chunks from the documents.")
    return chunks
