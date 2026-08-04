import json
from src.utils.model_loader import model_wrapper

def run_router_agent(user_query: str) -> dict:
    system_prompt = (
        "You are an intent and language classification system for Sri Lankan Higher Education. "
        "Return JSON with keys: language ('Sinhala','Tamil','English'), intent ('Academic','Welfare','Administrative','General'), search_query."
    )
    raw_response = model_wrapper.call_groq(prompt=f"User Query: {user_query}", system_prompt=system_prompt)
    try:
        return json.loads(raw_response)
    except Exception:
        return {"language": "English", "intent": "General", "search_query": user_query}
