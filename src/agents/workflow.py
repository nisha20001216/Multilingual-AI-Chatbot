from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from src.agents.router_agent import run_router_agent
from src.agents.rag_agent import run_rag_agent
from src.agents.reflection_agent import run_reflection_agent

class GraphState(TypedDict):
    user_query: str
    detected_language: str
    intent: str
    search_query: str
    retrieved_contexts: List[Dict[str, Any]]
    draft_answer: str
    final_response: str

def router_node(state: GraphState) -> GraphState:
    res = run_router_agent(state["user_query"])
    state["detected_language"] = res.get("language", "English")
    state["intent"] = res.get("intent", "General")
    state["search_query"] = res.get("search_query", state["user_query"])
    return state

def rag_node(state: GraphState) -> GraphState:
    res = run_rag_agent(state["search_query"])
    state["draft_answer"] = res["draft_answer"]
    state["retrieved_contexts"] = res["contexts"]
    return state

def reflection_node(state: GraphState) -> GraphState:
    final_res = run_reflection_agent(
        user_query=state["user_query"],
        target_language=state["detected_language"],
        draft_answer=state["draft_answer"],
        context_docs=state["retrieved_contexts"]
    )
    state["final_response"] = final_res
    return state

builder = StateGraph(GraphState)
builder.add_node("router", router_node)
builder.add_node("rag", rag_node)
builder.add_node("reflection", reflection_node)
builder.set_entry_point("router")
builder.add_edge("router", "rag")
builder.add_edge("rag", "reflection")
builder.add_edge("reflection", END)

app_workflow = builder.compile()

def process_query(user_query: str) -> dict:
    return app_workflow.invoke({
        "user_query": user_query, "detected_language": "", "intent": "",
        "search_query": "", "retrieved_contexts": [], "draft_answer": "", "final_response": ""
    })
