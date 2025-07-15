import pandas as pd
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

df = pd.read_csv("data/IDC_Chatbot_data.csv")

text_block = (df["question"] + " " + df["answer"]).astype(str).tolist()

#embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

#cromadb creation 
vectordb = Chroma.from_texts(
    texts=text_block,
    embedding=embedding_model,
    persist_directory="chroma_db"  )

vectordb.persist() #savse to disk
print("DB created")
