import streamlit as st
import pdfplumber
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

st.set_page_config(page_title="Wendeware Chatbot", layout="centered")
st.title("🤖 Wendeware Hybrid Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- RULE-BASED RESPONSES ---
def rule_based_response(query):
    q = query.lower()
    if any(x in q for x in ["hello", "hi"]):
        return "Hello! I'm the Wendeware chatbot. Ask me about AMPERIX®, myPowerGrid, or compatible devices."
    elif "amperix" in q:
        return "AMPERIX® is Wendeware’s modular EMS that controls solar, battery, grid and loads."
    elif "mypowergrid" in q or "portal" in q:
        return "myPowerGrid is a portal for visualizing energy and accessing your AMPERIX® system remotely."
    elif "tariff" in q or "stromtarif" in q:
        return "AMPERIX® supports dynamic tariffs from Tibber, aWATTar, and others."
    elif "ripple" in q or "rundsteuerempfänger" in q:
        return "Ripple control lets grid operators control loads remotely through AMPERIX®."
    elif "edition" in q:
        return "AMPERIX® comes in PURE, PLUS, and PRO editions with increasing features."
    elif "oem" in q:
        return "OEMs can integrate AMPERIX® into their own hardware or branding."
    elif "support" in q or "manual" in q:
        return "Find docs at https://manual.wendeware.com and support at https://www.wendeware.com/service-und-support"
    elif "about" in q or "wendeware" in q:
        return "Wendeware AG is a German company focusing on energy automation."
    return None

# --- LOAD AND INDEX PDF ---
@st.cache_resource
def load_pdf_qa():
    with pdfplumber.open("compatibility.pdf") as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    with open("compatibility.txt", "w") as f:
        f.write(text)
    loader = TextLoader("compatibility.txt")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    split_docs = splitter.split_documents(docs)
    vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )
    return qa_chain

qa_chain = load_pdf_qa()

# --- CHAT HANDLER ---
user_input = st.chat_input("Ask anything about AMPERIX®, tariffs, or compatibility...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = rule_based_response(user_input)
    if not response:
        with st.spinner("Searching compatibility list..."):
            response = qa_chain.run(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# Display history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
