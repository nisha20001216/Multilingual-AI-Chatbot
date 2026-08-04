from src.utils.model_loader import model_wrapper

def run_reflection_agent(user_query: str, target_language: str, draft_answer: str, context_docs: list) -> str:
    system_prompt = f"Refine and translate final output to {target_language}. Keep Sri Lankan university academic terms accurate."
    context_str = "\n".join([c["content"] for c in context_docs])
    prompt = f"Query: {user_query}\nContext: {context_str}\nDraft Answer: {draft_answer}\nProvide refined {target_language} output:"
    return model_wrapper.call_openrouter(prompt=prompt, system_prompt=system_prompt)
