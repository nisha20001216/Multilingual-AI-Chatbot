# Multilingual AI Chatbots for Student Support Services in Sri Lankan Universities

A production-ready, multi-agent Retrieval-Augmented Generation (RAG) system built with Streamlit, LangGraph, ChromaDB, Groq API, and OpenRouter API to provide trilingual (Sinhala, Tamil, English) academic and administrative guidance.

## Architecture

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

## Setup Instructions

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

4. **Run Evaluation Script**:
   ```bash
   python evaluation/rag_eval.py
   ```
