import streamlit as st
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Wendeware Chatbot", layout="centered")
st.title("🤖 Wendeware Hybrid Chatbot")

# --- INITIAL SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HELPER: Rule-Based Response ---
def rule_based_response(query):
    q = query.lower()
    if any(x in q for x in ["hello", "hi"]):
        return "Hello! I'm the Wendeware chatbot. Ask me about AMPERIX®, myPowerGrid, or supported devices."

    elif "amperix" in q:
        return "AMPERIX® is Wendeware’s modular energy management system that controls solar, grid, battery and loads."

    elif "mypowergrid" in q or "portal" in q:
        return "myPowerGrid is the web portal for visualizing energy flows and managing your AMPERIX® system remotely."

    elif "tariff" in q or "stromtarif" in q:
        return "AMPERIX® supports dynamic electricity tariffs from Tibber, aWATTar, and others."

    elif "ripple" in q or "rundsteuerempfänger" in q:
        return "Ripple control receivers let grid operators control loads remotely via AMPERIX®."

    elif "edition" in q:
        return "AMPERIX® comes in PURE, PLUS, and PRO editions with increasing functionality."

    elif "oem" in q:
        return "OEMs can integrate AMPERIX® into their own systems or rebrand it."

    elif "manual" in q or "support" in q or "documentation" in q:
        return "Find documentation at https://manual.wendeware.com and support at https://www.wendeware.com/service-und-support"

    elif "about" in q or "company" in q:
        return "Wendeware AG is a German company specializing in intelligent energy automation and control."

    return None  # Fall back to PDF if unknown

# --- LOAD PDF & INDEX ONCE ---
@st.cache_resource
def load_pdf_qa():
    loader = UnstructuredPDFLoader("compatibility.pdf")
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = splitter.split_documents(pages)

    vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    return qa

qa_chain = load_pdf_qa()

# --- CHAT LOGIC ---
user_input = st.chat_input("Ask anything about Wendeware or compatibility...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Try rule-based first
    answer = rule_based_response(user_input)
    if not answer:
        with st.spinner("Searching compatibility list..."):
            answer = qa_chain.run(user_input)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

# Show history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
