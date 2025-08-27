# src/project/app_streamlit.py
import streamlit as st
from crew import incidentHandling

def run_crew(user_input: str):
    """
    Ejecuta el crew con el input del usuario y devuelve la salida.
    """
    inputs = {'input': user_input}
    crew_instance = incidentHandling().crew()
    result = crew_instance.kickoff(inputs=inputs)
    return result

# ---- Interfaz Streamlit ----
st.set_page_config(page_title="Incident Handling Assistant", page_icon="🛠️")

st.title("🛠️ Incident Handling Assistant")
st.write("Haz preguntas o describe un incidente y el asistente lo procesará.")

# Input del usuario
user_input = st.text_area("Describe tu incidente aquí:", height=150)

if st.button("Procesar"):
    if user_input.strip():
        with st.spinner("Analizando el incidente..."):
            result = run_crew(user_input)

        st.success("✅ Análisis completo")
        st.subheader("Respuesta del asistente:")
        st.write(result)   # Aquí puede ser dict o str, según CrewAI
    else:
        st.warning("⚠️ Por favor escribe un incidente antes de procesar.")
