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

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# -----------------------------
# Configuration
# -----------------------------
EMBEDDINGS_MODEL = "text-embedding-ada-002"

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
# Helpers
# -----------------------------
def fetch_text(url: str) -> str:
    """
    Fetches and cleans the text content of a web page.
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
        return "\n".join(lines)
    except Exception:
        return ""

# -----------------------------
# Vector Store Initialization
# -----------------------------
def get_vectorstore():
    """
    Builds an in-memory FAISS vector store from the provided URLs.
    """
    all_text = ""
    for url in URLS:
        st.write(f"Fetching {url}")
        all_text += fetch_text(url) + "\n"

    splitter = CharacterTextSplitter(separator="\n", chunk_size=800, chunk_overlap=200)
    docs = splitter.split_text(all_text)

    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL, openai_api_key=API_KEY)
    store = FAISS.from_texts(texts=docs, embedding=embeddings)
    return store

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="WendeWare Q&A Bot", layout="wide")
st.title("WendeWare Interview Chatbot")

# Retrieve OpenAI key from Streamlit secrets
API_KEY = st.secrets.get("OPENAI_API_KEY")
if not API_KEY:
    st.error("🔑 Please add your OpenAI API key to Streamlit Secrets as OPENAI_API_KEY.")
    st.stop()

# Build vector store and QA chain
with st.spinner("Building knowledge base—this may take a minute..."):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = OpenAI(openai_api_key=API_KEY)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Chat interface
query = st.text_input("Ask me anything about WendeWare:")
if query:
    with st.spinner("Thinking..."):
        answer = qa_chain.run(query)
    st.markdown("**Answer:**")
    st.write(answer)
