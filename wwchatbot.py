import streamlit as st

st.set_page_config(page_title="Wendeware Chatbot", layout="centered")

st.title("🤖 Wendeware Product Chatbot")
st.write("Ask me anything about Wendeware, AMPERIX®, or energy management topics!")

user_input = st.text_input("Your Question:")

if user_input:
    query = user_input.lower()

    if "amperix" in query:
        st.markdown("**AMPERIX®** is Wendeware’s modular energy management system (EMS) designed to monitor, optimize, and control the flow of energy between solar panels, batteries, the grid, and electrical loads.")
    elif "mypowergrid" in query or "portal" in query:
        st.markdown("**myPowerGrid** is a web-based portal by Wendeware that provides a real-time view of energy flows, device management, and consumption analysis.")
    elif "dynamic tariff" in query or "stromtarif" in query:
        st.markdown("AMPERIX® supports dynamic electricity tariffs from providers like Tibber, aWATTar, and Octopus Energy, enabling users to optimize energy usage and reduce costs.")
    elif "ripple" in query or "rundsteuerempfänger" in query:
        st.markdown("Wendeware integrates **ripple control receivers** into its AMPERIX® EMS, allowing communication with distribution grid operators for demand control.")
    elif "edition" in query:
        st.markdown("AMPERIX® is available in **PURE**, **PLUS**, and **PRO** editions. Each edition adds more functionalities such as direct marketing, tariff optimization, and smart load control.")
    elif "oem" in query:
        st.markdown("The OEM program enables other companies to integrate AMPERIX® functionalities into their hardware or services under their own branding.")
    elif "support" in query or "manual" in query:
        st.markdown("You can find documentation and technical support in the [Wendeware Manual Portal](https://manual.wendeware.com/) and the [Support Page](https://www.wendeware.com/service-und-support).")
    elif "company" in query or "about" in query:
        st.markdown("Wendeware AG is a German company specializing in intelligent energy systems and automation technologies. More at [About Us](https://www.wendeware.com/ueber-uns).")
    else:
        st.write("I'm still learning. Try asking about AMPERIX®, myPowerGrid, tariffs, editions, or OEM features.")
