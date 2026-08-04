import time
from src.agents.workflow import process_query

TEST_QUERIES = [
    {"query": "මහපොළ ශිෂ්‍යත්වය සඳහා සුදුසුකම් මොනවාද?", "expected_lang": "Sinhala", "category": "Welfare"},
    {"query": "விடுதி விண்ணப்ப முறை என்ன?", "expected_lang": "Tamil", "category": "Administrative"},
    {"query": "What is the 14-day rule for medical submission?", "expected_lang": "English", "category": "Academic"},
    {"query": "How is GPA calculated and what are repeat exam rules?", "expected_lang": "English", "category": "Academic"},
    {"query": "What are the anti-ragging laws in Sri Lanka?", "expected_lang": "English", "category": "Administrative"}
]

def run_evaluation():
    print("=" * 60)
    print("RUNNING AGENTIC RAG SYSTEM EVALUATION")
    print("=" * 60)
    for idx, item in enumerate(TEST_QUERIES, 1):
        q = item["query"]
        start_time = time.time()
        res = process_query(q)
        elapsed = time.time() - start_time
        print(f"\n[Test {idx}/5] Query: {q}")
        print(f" Detected Lang: {res['detected_language']} | Intent: {res['intent']} | Chunks: {len(res['retrieved_contexts'])} | Latency: {elapsed:.2f}s")

if __name__ == "__main__":
    run_evaluation()
