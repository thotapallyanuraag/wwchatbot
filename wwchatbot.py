import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="Wendeware Chatbot",
    page_icon="⚡",
    layout="centered",
)

# --- Logo and Title ---
st.image("https://www.wendeware.com/_files/ugd/24a36c_ba5bed91b1b1411091a13b7313ed3e6c.pdf", width=100)
st.title("🤖 Wendeware Product Chatbot")
st.markdown(
    """
Welcome! This chatbot helps you learn about Wendeware's energy solutions like **AMPERIX®**, **myPowerGrid**, and more.

Ask me anything about:
- AMPERIX® Editions (PURE, PLUS, PRO)
- Dynamic Tariffs
- Ripple Control
- OEM Integration
- Support & Documentation

---
"""
)

# --- User Input ---
user_input = st.text_input("💬 Your Question:")

# --- Response Logic ---
if user_input:
    query = user_input.lower()

    if "amperix" in query:
        st.success("AMPERIX® is Wendeware’s modular energy management system that monitors, optimizes, and controls the flow of energy between solar panels, batteries, the grid, and electrical loads.")
    elif "mypowergrid" in query or "portal" in query:
        st.success("myPowerGrid is a cloud-based portal that visualizes energy flows, tracks system performance, and allows remote access to the AMPERIX® system.")
    elif "tariff" in query or "stromtarif" in query:
        st.success("AMPERIX® supports dynamic tariffs from Tibber, aWATTar, and others to optimize your electricity usage and save costs.")
    elif "ripple" in query or "rundsteuerempfänger" in query:
        st.success("Ripple control receivers integrated with AMPERIX® allow remote load control by distribution grid operators.")
    elif "edition" in query:
        st.success("AMPERIX® is available in PURE, PLUS, and PRO editions offering scalability from basic to advanced energy control features.")
    elif "oem" in query:
        st.success("AMPERIX® OEM enables integration into partner hardware or custom-branded platforms.")
    elif "manual" in query or "support" in query:
        st.success("Find detailed docs at https://manual.wendeware.com and technical support at https://www.wendeware.com/service-und-support.")
    elif "company" in query or "about" in query:
        st.success("Wendeware AG is a German company focusing on intelligent energy automation. Learn more at https://www.wendeware.com/ueber-uns.")
    else:
        st.warning("I'm still learning. Try asking about AMPERIX®, tariffs, ripple control, or OEM features.")
