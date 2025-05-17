# import streamlit as st

# st.set_page_config(page_title="Wendeware Chatbot", layout="centered")
# st.title("🤖 Wendeware Local Chatbot")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # --- Rule-Based Answering System ---
# def rule_based_response(query):
#     q = query.lower()
#     if any(x in q for x in ["hello", "hi", "hey"]):
#         return "Hello! I'm the Wendeware chatbot. Ask me about AMPERIX®, myPowerGrid, or compatible devices."
#     elif "amperix" in q:
#         return "AMPERIX® is Wendeware’s modular energy management system that controls solar, battery, grid, and loads."
#     elif "mypowergrid" in q or "portal" in q:
#         return "myPowerGrid is the web portal to visualize energy and access your AMPERIX® system remotely."
#     elif "tariff" in q or "stromtarif" in q:
#         return "AMPERIX® supports dynamic electricity tariffs like Tibber and aWATTar."
#     elif "ripple" in q or "rundsteuerempfänger" in q:
#         return "Ripple control allows grid operators to control AMPERIX® connected devices remotely."
#     elif "edition" in q:
#         return "AMPERIX® is available in PURE, PLUS, and PRO editions with increasing features."
#     elif "oem" in q:
#         return "OEMs can integrate AMPERIX® into their own hardware or branding."
#     elif "support" in q or "manual" in q:
#         return "Visit https://manual.wendeware.com or https://wendeware.com/service-und-support for documentation and help."
#     elif "about" in q or "wendeware" in q:
#         return "Wendeware AG is a German company focused on smart energy automation."
#     else:
#         return "I'm a local chatbot. Please ask about AMPERIX®, myPowerGrid, tariffs, or compatible devices."

# # --- Chat UI ---
# user_input = st.chat_input("Ask me anything about Wendeware...")

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     st.chat_message("user").write(user_input)

#     response = rule_based_response(user_input)
#     st.session_state.messages.append({"role": "assistant", "content": response})
#     st.chat_message("assistant").write(response)

# # Show history
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])


import requests
from bs4 import BeautifulSoup
import streamlit as st

# -----------------------------
# Configuration
# -----------------------------
URLS = [
    "https://www.wendeware.com/",
    "https://www.wendeware.com/amperix-energiemanagementsystem",
    "https://www.wendeware.com/amperix-energiemanager",
    "https://www.wendeware.com/amperix-portal-mypowergrid",
    "https://www.wendeware.com/amperix-funktionen",
    "https://www.wendeware.com/rundsteuerempfaenger",
    "https://www.wendeware.com/dynamische-stromtarife",
    "https://www.wendeware.com/amperix-editionen",
    "https://www.wendeware.com/amperix-oem",
    "https://www.wendeware.com/ueber-uns",
    "https://www.wendeware.com/jobs",
    "https://www.wendeware.com/kontakt",
    "https://www.wendeware.com/produktsicherheit",
    "https://www.wendeware.com/service-und-support",
    "https://manual.wendeware.com/",
    "https://www.wendeware.com/kompatibilitaetsliste",
]

# -----------------------------
# Page Fetching & Caching
# -----------------------------
@st.cache_data(show_spinner=False)
def load_pages():
    data = {}
    for url in URLS:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            text = "\n".join(
                [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
            )
            data[url] = text
        except Exception:
            data[url] = ""
    return data

pages = load_pages()

# -----------------------------
# Streamlit App Setup
# -----------------------------
st.set_page_config(page_title="WendeWare Interview Chatbot", layout="wide")
st.title("WendeWare Interview Chatbot")

# Load API key from secrets
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("🔑 Please add your OpenAI API key to Streamlit Secrets (OPENAI_API_KEY).")
    st.stop()

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# -----------------------------
# Chat Interface
# -----------------------------
query = st.text_input("Ask me anything about WendeWare:")
if query:
    with st.spinner("Generating response..."):
        # Build context from all pages (truncate each to avoid huge payload)
        context = "\n\n".join(
            f"URL: {url}\nCONTENT:\n{pages[url][:2000]}"
            for url in pages
        )
        messages = [
            {"role": "system", "content": "You are an expert assistant on WendeWare products. Use only the provided documentation."},
            {"role": "user", "content": f"Documentation:\n{context}\n\nQuestion: {query}"}
        ]
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 500
        }
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        try:
            resp.raise_for_status()
            answer = resp.json()["choices"][0]["message"]["content"]
        except Exception:
            st.error("⚠️ Error fetching completion. Check your API key and rate limits.")
            st.stop()
    st.markdown("**Answer:**")
    st.write(answer)




