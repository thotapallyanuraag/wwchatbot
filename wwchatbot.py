import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Wendeware Chatbot", layout="centered")
st.title("🤖 Wendeware Hybrid Chatbot (No FAISS)")

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

# --- LOAD TEXT CONTEXT ---
@st.cache_resource
def load_pdf_text():
    with open("compatibility_text.txt", "r", encoding="utf-8") as f:
        return f.read()

context_text = load_pdf_text()

# --- GPT CONTEXT Q&A ---
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
template = """
You are an expert on Wendeware products. Use the following context to answer:

Context:
{context}

Question:
{question}
"""
prompt = PromptTemplate.from_template(template)
qa_chain = LLMChain(llm=llm, prompt=prompt)

# --- CHAT HANDLER ---
user_input = st.chat_input("Ask anything about AMPERIX®, tariffs, or compatibility...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = rule_based_response(user_input)
    if not response:
        with st.spinner("Searching compatibility info..."):
            response = qa_chain.run({"context": context_text, "question": user_input})

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
