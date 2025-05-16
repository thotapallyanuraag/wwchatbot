import streamlit as st

st.set_page_config(page_title="Wendeware Chatbot", layout="centered")
st.title("🤖 Wendeware Local Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Rule-Based Answering System ---
def rule_based_response(query):
    q = query.lower()
    if any(x in q for x in ["hello", "hi", "hey"]):
        return "Hello! I'm the Wendeware chatbot. Ask me about AMPERIX®, myPowerGrid, or compatible devices."
    elif "amperix" in q:
        return "AMPERIX® is Wendeware’s modular energy management system that controls solar, battery, grid, and loads."
    elif "mypowergrid" in q or "portal" in q:
        return "myPowerGrid is the web portal to visualize energy and access your AMPERIX® system remotely."
    elif "tariff" in q or "stromtarif" in q:
        return "AMPERIX® supports dynamic electricity tariffs like Tibber and aWATTar."
    elif "ripple" in q or "rundsteuerempfänger" in q:
        return "Ripple control allows grid operators to control AMPERIX® connected devices remotely."
    elif "edition" in q:
        return "AMPERIX® is available in PURE, PLUS, and PRO editions with increasing features."
    elif "oem" in q:
        return "OEMs can integrate AMPERIX® into their own hardware or branding."
    elif "support" in q or "manual" in q:
        return "Visit https://manual.wendeware.com or https://wendeware.com/service-und-support for documentation and help."
    elif "about" in q or "wendeware" in q:
        return "Wendeware AG is a German company focused on smart energy automation."
    else:
        return "I'm a local chatbot. Please ask about AMPERIX®, myPowerGrid, tariffs, or compatible devices."

# --- Chat UI ---
user_input = st.chat_input("Ask me anything about Wendeware...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = rule_based_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# Show history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
