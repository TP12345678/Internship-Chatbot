import pandas as pd
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from ppt_data import extract_text_from_pptx_with_images

#df = pd.read_csv("data/IDC_Chatbot_data.csv")
ppt_data = extract_text_from_pptx_with_images("/Users/tushi/Internship-Chatbot/backend/data/IDC Digital Corporate Deck- Middle East- V1.pptx")

#text_block = (df["question"] + " " + df["answer"]).astype(str).tolist()

#embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

#cromadb creation 
vectordb = Chroma.from_texts(
    texts=ppt_data,
    embedding=embedding_model,
    persist_directory="chroma_db"  )

vectordb.persist() #savse to disk
print("DB created")
