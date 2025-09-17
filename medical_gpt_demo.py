import os
import streamlit as st
import numpy as np

# --- Demo mode flag ---
DEMO_MODE = True  # True = no API call, just dummy response

st.set_page_config(page_title="Medical GPT Demo", layout="wide")
st.title("🧠 Medical GPT Demo")
st.caption("Prototype — not for clinical use")

# --- Sidebar for API key (optional) ---
if not DEMO_MODE:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
else:
    api_key = None
    st.sidebar.info("Running in DEMO MODE — no API key needed.")

# --- Question Input ---
query = st.text_area("Enter a medical question:", height=100)

if st.button("Ask"):
    if DEMO_MODE:
        # Dummy response (pretend LLM + retrieval)
        st.subheader("Answer")
        st.markdown(
            """Guidelines recommend **Metformin** as first-line treatment for type 2 diabetes
            unless contraindicated. Lifestyle modifications (diet, exercise) are strongly encouraged.

            **Sources:**
            1. ADA Standards of Medical Care in Diabetes — 2023
            2. UpToDate: Initial management of hyperglycemia in adults"""
        )
    else:
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        else:
            with st.spinner("Querying model..."):
                # Normally here you would run retrieval + LLM call
                # Example: answer = ask_medical_gpt(query, api_key)
                st.subheader("Answer")
                st.write("(Real API call result would appear here.)")
