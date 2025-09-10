# src/project/app_streamlit.py
import streamlit as st
import pandas as pd
from crew import incidentHandling
import json
import datetime

# ---- Paths ----
detect_area_path = "..\\project\\output\\detect_area.json"
detect_category_path = "..\\project\\output\\detect_category.json"
sentiment_analysis_path = "..\\project\\output\\sentiment_analysis.json"

def load_json():
    with open(detect_area_path, "r", encoding="utf-8") as a:
        detect_area_output = json.load(a)

    with open(detect_category_path, "r", encoding="utf-8") as c:
        detect_category_output = json.load(c)

    with open(sentiment_analysis_path, "r", encoding="utf-8") as s:
        sentiment_analysis_output = json.load(s)

    return detect_area_output, detect_category_output, sentiment_analysis_output

def run_crew(user_input: str):
    """Ejecuta el crew con el input del usuario y guarda resultados en JSON"""
    inputs = {'input': user_input}
    crew_instance = incidentHandling().crew()
    crew_instance.kickoff(inputs=inputs)


# ---- Interface Streamlit ----
st.set_page_config(page_title="Incident Handling Assistant", page_icon="🛠️", layout="centered")

st.title("🛠️ Incident Handling Assistant with CrewAI Agents")
st.subheader("Groq-LLaMa 3.1 - CrewAI Framework - Streamlit - Pandas")
st.markdown("---")

# Links
columns = st.columns((1, 1, 1))
with columns[0]:
    st.page_link('https://www.linkedin.com/in/yeins-aristizabal/', label="LinkedIn")
with columns[1]:
    st.page_link('https://github.com/YeinsAristizabal/ai/tree/main/intelligent-incident-agent', label="GitHub")
with columns[2]:
    st.markdown("**Developed by Yeins Aristizabal**")

st.markdown("---")
st.write("Describe an incident and the assistant will process it.")

# ---- Input ----
user_input = st.text_area("Describe your incident here:", height=150)

if st.button("Process"):
    if user_input.strip():
        with st.spinner("Analyzing the incident..."):
            run_crew(user_input)

        detect_area_output, detect_category_output, sentiment_analysis_output = load_json()

        # Save last analysis in session_state
        st.session_state.last_input = user_input
        st.session_state.last_category = detect_category_output['category']
        st.session_state.last_area = detect_area_output['area']
        st.session_state.last_sentiment = sentiment_analysis_output['sentiment']

        st.success("✅ Full analysis completed")
    else:
        st.warning("⚠️ Please report an incident before proceeding.")


# ---- Show last analysis (if exists) ----
if "last_category" in st.session_state:
    st.subheader("Latest analysis")
    st.metric("Category", st.session_state.last_category)
    st.metric("Area", st.session_state.last_area)
    st.metric("Sentiment", st.session_state.last_sentiment)

# ---- Load historical dataframe ----
st.markdown("---")
if "df" not in st.session_state:
    st.session_state.df = pd.read_excel("..\\..\\data\\incidents.xlsx")

df = st.session_state.df

# KPIs historicos
negatives = len(df[df["sentiment"]=="Negative"])
positives = len(df[df["sentiment"]=="Positive"])
neutral = len(df[df["sentiment"]=="Neutral"])

st.subheader("Historical incidents")
st.metric("Total number of incidents reported", len(df))
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total positive incidents", positives)
with col2:
    st.metric("Total negative incidents", negatives)
with col3:
    st.metric("Total neutral incidents", neutral)

# ---- Update DB button ----
if st.button("Send request and update database"):
    if "last_input" in st.session_state:
        new_row = pd.DataFrame({
            "pqr_text": [st.session_state.last_input],
            "category": [st.session_state.last_category],
            "area": [st.session_state.last_area],
            "sentiment": [st.session_state.last_sentiment],
            "date": [datetime.datetime.now()]
        })
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.success("✅ Request added to database (in-memory)")
    else:
        st.warning("⚠️ Please process an incident before sending.")

st.dataframe(st.session_state.df)