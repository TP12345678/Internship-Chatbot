from langchain_text_splitters import RecursiveCharacterTextSplitter

# Text Processing Configuration (can be moved to config.py if preferred)
CHUNK_SIZE = 1500  # Increased chunk size to try and keep more of a logical section together
CHUNK_OVERLAP = 150 # Adjusted overlap

def chunk_text(documents):
    """
    Chunks the extracted text documents into smaller, manageable pieces,
    using universal separators to handle diverse document structures.
    Returns a list of dictionaries, each containing 'chunk_id', 'text', and 'source'.
    """
    # Define a robust list of universal separators, ordered from largest/most semantic to smallest.
    # This strategy is more adaptable to future documents that may not follow specific case study formats.
    separators = [
        "\n\n\n",  # Three newlines (often indicates a very significant break, like a new section/page)
        "\n\n",    # Double newline (standard paragraph break)
        "\n",      # Single newline (line break)
        " ",       # Space (splits words)
        ""         # Fallback for individual characters
    ]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False, # Keeping this as False as our separators are literal strings
        separators=separators # Apply universal separators
    )
    
    chunks = []
    chunk_id_counter = 0
    for doc in documents:
        # Clean text: replace multiple spaces/newlines with single ones for better chunking
        # This is important before splitting to standardize whitespace
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
