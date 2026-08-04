from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import config

class RAGRetriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
        self.vector_db = Chroma(persist_directory=str(config.CHROMA_DB_DIR), embedding_function=self.embeddings)

    def retrieve(self, query: str, top_k: int = config.TOP_K_RESULTS):
        results = self.vector_db.similarity_search_with_score(query, k=top_k)
        retrieved_contexts = []
        for doc, score in results:
            retrieved_contexts.append({"content": doc.page_content, "source": doc.metadata.get("source", "Unknown"), "score": float(score)})
        return retrieved_contexts

retriever_instance = RAGRetriever()
