import os
import requests
from groq import Groq
import config

def get_secret(key_name: str) -> str:
    try:
        import streamlit as st
        if key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    return os.getenv(key_name, "")

class ModelClientWrapper:
    def __init__(self):
        self.groq_key = get_secret("GROQ_API_KEY")
        self.openrouter_key = get_secret("OPENROUTER_API_KEY")
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key and self.groq_key != "your_groq_api_key_here" else None

    def call_groq(self, prompt: str, system_prompt: str = "You are a helpful academic assistant.") -> str:
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model=config.GROQ_MODEL,
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                    temperature=0.1, max_tokens=300
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"[Groq Fallback]: {e}")
        return self._mock_router_fallback(prompt)

    def call_openrouter(self, prompt: str, system_prompt: str = "") -> str:
        if self.openrouter_key and self.openrouter_key != "your_openrouter_api_key_here":
            try:
                headers = {"Authorization": f"Bearer {self.openrouter_key}", "Content-Type": "application/json"}
                payload = {"model": config.OPENROUTER_MODEL, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}], "temperature": 0.2}
                res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=10)
                if res.status_code == 200:
                    return res.json()["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"[OpenRouter Fallback]: {e}")
        return self._mock_rag_fallback(prompt)

    def _mock_router_fallback(self, prompt: str) -> str:
        lang = "English"
        if any(c in prompt for c in ["ම", "හ", "ප", "ො", "ළ", "ශ", "්", "ය"]):
            lang = "Sinhala"
        elif any(c in prompt for c in ["வ", "ி", "டு", "தி"]):
            lang = "Tamil"

        intent = "General"
        if "mahapola" in prompt.lower() or "bursary" in prompt.lower() or "මහපොළ" in prompt:
            intent = "Welfare"
        elif "gpa" in prompt.lower() or "exam" in prompt.lower() or "medical" in prompt.lower():
            intent = "Academic"
        elif "hostel" in prompt.lower() or "விடுதி" in prompt:
            intent = "Administrative"

        return f'{{"language": "{lang}", "intent": "{intent}", "search_query": "{prompt}"}}'

    def _mock_rag_fallback(self, prompt: str) -> str:
        return f"Based on University Regulations:\n\nRegarding your request:\n{prompt[:300]}...\n\nPlease check student division guidelines for updated forms and procedure submission deadlines."

model_wrapper = ModelClientWrapper()
