# Multilingual AI Chatbots for Student Support Services in Sri Lankan Universities

**Module:** IT41043 - Intelligent Systems (Agentic AI)  
**Institution:** Horizon Campus  
**Student Name:** Nipuni Malsha (ITBIN-2313-0023)

Build a production-ready, multi-agent RAG application in Python using Streamlit, LangGraph, ChromaDB, Groq API, and OpenRouter API to deliver trilingual (Sinhala, Tamil, English) student support for Sri Lankan Higher Education.

## Architecture & Design Patterns
## Multi-Agent Workflow (LangGraph StateGraph)
The core workflow uses a state-driven multi-agent Graph containing:

### 1. Router Agent:

**Language Identification:** Detects whether the query is in Sinhala, Tamil, or English (including Singlish/Tanglish transliterations).
**Intent Classification:** Classifies into Academic, Welfare, Administrative, or General.
**Query Translation & Reformulation:** Converts native/informal queries into optimized English search queries for dense embedding retrieval while preserving user intent.
**Model Used:** Groq API (llama-3.1-8b-instant) for ultra-low latency (<300ms) execution.

### 2. RAG Knowledge Retriever & Synthesizer Agent (ReAct Pattern):
**ReAct Loop:** Decides dynamically whether local vector RAG context is required or if general fallback knowledge/formatting applies.
**Context Retrieval:** Queries ChromaDB vector store using sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2.
**Draft Answer Generation:** Generates ground-truth answer based strictly on retrieved university guidelines and policies.
**Model Used:** OpenRouter API (anthropic/claude-3.5-sonnet or meta-llama/llama-3.3-70b-instruct / google/gemini-2.5-flash).

### 3. Reflection & Self-Critique Agent:
**Faithfulness Check:** Verifies draft output against original RAG contexts to eliminate hallucinations.
**Multilingual Quality & Cultural Nuance:** Refines the response into fluent Sinhala, Tamil, or English depending on user preference, maintaining polite academic tone (e.g. Sri Lankan university terminology like Mahapola, UGC, GPA, Medical Submission within 14 Days).
**Fallback/Regeneration:** Triggers refinement if confidence is low.

### 4. Architecture
```
[ User Query ]
      │
      ▼
┌──────────────┐   Groq API (llama-3.1-8b-instant)
│ Router Agent │ ──► Language Detection & Intent Classification
└──────┬───────┘
       │
       ▼
┌──────────────┐   ChromaDB + sentence-transformers
│  RAG Agent   │ ──► ReAct Dense Retrieval & Draft Synthesis
└──────┬───────┘
       │
       ▼
┌──────────────┐   OpenRouter API (claude-3.5-sonnet)
│ Reflection   │ ──► Faithfulness Verification & Trilingual Translation
│    Agent     │
└──────┬───────┘
       │
       ▼
[ Final Answer ]
```

## 5. Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ingest Knowledge Base**:
   ```bash
   python src/rag/ingest.py
   ```

3. **Run Application**:
   ```bash
   streamlit run app.py
   ```
   ```bash

## 6. Verification Plan

**Automated Tests & Evaluation**
Execute python evaluation/rag_eval.py:
-Runs 5 target validation queries (covering Sinhala, Tamil, English, Academic, Welfare).
-Evaluates retrieval precision, context recall, answer relevancy, and response latency.
-Outputs a detailed performance report.

**Manual UI Verification**
-Launch Streamlit app via streamlit run app.py.
-Test Sinhala ("මහපොළ ශිෂ්‍යත්වය සඳහා සුදුසුකම් මොනවාද?"), Tamil ("விடுதி விண்ணப்ப முறை என்ன?"), and English queries.
-Inspect Agent execution steps (Router classification -> ReAct context retrieval -> Reflection self-critique).
-Verify vector DB ingestion via the UI sidebar trigger or CLI python src/rag/ingest.py.

 ## 7. Repository Structure

 ├── .streamlit/
│   └── secrets.toml             # API key templates & configuration defaults
├── .gitignore                   # Ignores __pycache__, vector store binaries, .env
├── README.md                    # Detailed documentation & deployment guide for Streamlit Cloud
├── requirements.txt             # Python dependencies (streamlit, langgraph, chromadb, etc.)
├── app.py                       # Main Streamlit UI application
├── config.py                    # Global configurations, model paths, system settings
├── data/
│   └── university_docs/         # 20+ domain knowledge files (Markdown & TXT)
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── router_agent.py      # Language & Intent classifier agent
│   │   ├── rag_agent.py         # ReAct RAG retriever & synthesizer agent
│   │   ├── reflection_agent.py  # Self-critique & translation refiner agent
│   │   └── workflow.py          # LangGraph execution workflow setup
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingest.py            # Vector ingestion & RecursiveCharacterTextSplitter
│   │   └── retriever.py         # ChromaDB retrieval & semantic search
│   └── utils/
│       ├── __init__.py
│       └── model_loader.py      # Groq & OpenRouter API client wrapper with fallback
└── evaluation/
    └── rag_eval.py              # Automated precision, recall & relevancy test script
   python evaluation/rag_eval.py
   ```
