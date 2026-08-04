import streamlit as st
from src.rag.ingest import run_ingestion
from src.agents.workflow import process_query

st.set_page_config(
    page_title="Sri Lankan University Student Support AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Sri Lankan University Support Bot")
st.subheader("Trilingual Multi-Agent Assistant (Sinhala | Tamil | English)")

with st.sidebar:
    st.header("⚙️ Administrative Control")
    st.info("System operational using ChromaDB, Groq API & OpenRouter API.")
    
    if st.button("Re-ingest Knowledge Base"):
        with st.spinner("Processing 20+ markdown documents..."):
            run_ingestion()
        st.success("Vector database updated successfully!")

    st.markdown("---")
    st.markdown("### Sample Prompts")
    st.markdown("- **Sinhala**: මහපොළ ශිෂ්‍යත්වය සඳහා සුදුසුකම් මොනවාද?")
    st.markdown("- **Tamil**: விடுதி விண்ணப்ப முறை என்ன?")
    st.markdown("- **English**: What is the 14-day rule for submitting medical certificates?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a question regarding university regulations...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.status("Agentic Workflow Processing...", expanded=True) as status:
            st.write("🔍 **Router Agent**: Detecting Language and Intent...")
            result = process_query(user_input)
            
            st.write(f"✓ Detected Language: `{result['detected_language']}` | Intent: `{result['intent']}`")
            st.write("📚 **RAG Agent**: Performing semantic search on ChromaDB...")
            st.write(f"✓ Retrieved `{len(result['retrieved_contexts'])}` context chunks.")
            st.write("✨ **Reflection Agent**: Checking faithfulness & translating output...")
            
            status.update(label="Processing Complete!", state="complete", expanded=False)

        st.markdown(result["final_response"])
        
        with st.expander("View Retrieved Knowledge Contexts"):
            for i, ctx in enumerate(result["retrieved_contexts"], 1):
                st.markdown(f"**Source {i}:** `{ctx['source']}`")
                st.caption(ctx["content"])

        st.session_state.messages.append({"role": "assistant", "content": result["final_response"]})
