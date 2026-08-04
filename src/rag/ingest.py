import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import config

def run_ingestion():
    loader = DirectoryLoader(str(config.DATA_DIR), glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=str(config.CHROMA_DB_DIR))
    print("Ingestion completed successfully.")

if __name__ == "__main__":
    run_ingestion()
