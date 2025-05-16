import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="Wendeware Chatbot", layout="centered")
st.title("🤖 Wendeware Product Chatbot")
st.markdown("Ask me anything about AMPERIX®, myPowerGrid, tariffs, ripple control, or support.")

# --- Initialize session state for messages ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Define response function ---
def get_bot_response(user_input):
    query = user_input.lower()

    if any(word in query for word in ["amperix", "ems", "energy manager"]):
        return "AMPERIX® is Wendeware’s modular energy management system that monitors, optimizes, and controls energy between solar panels, batteries, the grid, and loads."

    elif any(word in query for word in ["mypowergrid", "portal", "web interface"]):
        return "myPowerGrid is a cloud-based portal that shows energy flows, system status, and allows remote access to your AMPERIX® EMS."

    elif any(word in query for word in ["tariff", "stromtarif", "electricity price", "dynamic price"]):
        return "AMPERIX® supports dynamic tariffs from Tibber, aWATTar, and other providers to help reduce your electricity costs."

    elif any(word in query for word in ["ripple", "rundsteuerempfänger", "load control"]):
        return "Ripple control receivers let grid operators send remote control signals to AMPERIX® for managing energy loads."

    elif any(word in query for word in ["edition", "pure", "plus", "pro"]):
        return "AMPERIX® comes in PURE, PLUS, and PRO editions. Each edition adds more features, like direct marketing and smart load control."

    elif any(word in query for word in ["oem", "integration", "partner"]):
        return "OEM customers can integrate AMPERIX® into their own hardware and offer it under their own brand."

    elif any(word in query for word in ["manual", "documentation", "guide", "support", "help"]):
        return "You can find detailed documentation at https://manual.wendeware.com and support at https://www.wendeware.com/service-und-support."

    elif any(word in query for word in ["company", "about", "wendeware"]):
        return "Wendeware AG is a German company specializing in intelligent energy systems and automation."

    else:
        return "I'm still learning. Try asking about AMPERIX®, dynamic tariffs, ripple control, or support."

# --- Chat Display ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Chat Input ---
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get bot response
    response = get_bot_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
