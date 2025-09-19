import os
import streamlit as st
import numpy as np
import pandas as pd
import json
from datetime import datetime

# --- Demo mode flag ---
DEMO_MODE = True  # True = no API call, just dummy response

st.set_page_config(page_title="Medical GPT Demo", layout="wide")

# --- Session State: Log Storage ---
if "qa_logs" not in st.session_state:
    st.session_state.qa_logs = []  # her soru burada biriktirilecek

# --- Tabs: Hekim Asistanı + CMS Paneli ---
tab1, tab2 = st.tabs(["💬 Hekim Asistanı", "📊 CMS Paneli"])

# --- TAB 1: Hekim Asistanı ---
with tab1:
    st.title("🧠 Medical GPT Demo")
    st.caption("Prototype — not for clinical use")

    if not DEMO_MODE:
        api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    else:
        api_key = None
        st.sidebar.info("Running in DEMO MODE — no API key needed.")

    query = st.text_area("Enter a medical question:", height=100)

    if st.button("Ask", key="ask_btn"):
        # her soruyu session_state'e logla
        st.session_state.qa_logs.append({
            "doctor_id": np.random.randint(100, 999),  # sahte doktor id
            "question": query,
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "specialty": np.random.choice(["Pediatri", "Dahiliye", "Kardiyoloji"]),
            "avg_response_ms": np.random.randint(700, 1500)
        })

        if DEMO_MODE:
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
                    st.subheader("Answer")
                    st.write("(Real API call result would appear here.)")

# --- TAB 2: CMS Paneli ---
with tab2:
    st.title("CMS / Yönetim Paneli (Demo)")
    nl_query = st.text_input("Sorgu yazın (örn: Eylül’de gentamisin geçen konuşmalar)", key="cms_query")

    if st.button("Çalıştır", key="cms_run"):
        # Eğer kullanıcı sorgu yazmadıysa, son logları göster
        if nl_query.strip() == "":
            if len(st.session_state.qa_logs) > 0:
                df = pd.DataFrame(st.session_state.qa_logs)
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Export CSV",
                    data=csv,
                    file_name="all_logs.csv",
                    mime="text/csv",
                )
            else:
                st.warning("Henüz hiç soru sorulmadı.")
        else:
            # örnek filtre (gentamisin geçen sorular)
            filtered = [log for log in st.session_state.qa_logs if "gentamisin" in log["question"].lower()]
            if filtered:
                df = pd.DataFrame(filtered)
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Export CSV",
                    data=csv,
                    file_name="segment_results.csv",
                    mime="text/csv",
                )
                if st.button("Segment Kaydet"):
                    segment = {
                        "name": f"Segment-{datetime.now().isoformat()}",
                        "filter": nl_query,
                        "count": len(df)
                    }
                    with open("segments.json", "a") as f:
                        f.write(json.dumps(segment) + "\n")
                    st.success(f"Segment kaydedildi: {segment['name']}")
            else:
                st.warning("Bu sorguya uygun kayıt bulunamadı.")


