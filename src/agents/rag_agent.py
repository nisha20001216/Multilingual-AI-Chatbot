from src.rag.retriever import retriever_instance
from src.utils.model_loader import model_wrapper

def run_rag_agent(search_query: str) -> dict:
    retrieved_docs = retriever_instance.retrieve(search_query)
    context_text = "\n\n---\n\n".join([d["content"] for d in retrieved_docs])
    system_prompt = "You are a Sri Lankan University Academic Advisor. Answer accurately based on provided context."
    prompt = f"Context Material:\n{context_text}\n\nSearch Question: {search_query}"
    draft_answer = model_wrapper.call_openrouter(prompt=prompt, system_prompt=system_prompt)
    return {"draft_answer": draft_answer, "contexts": retrieved_docs}
