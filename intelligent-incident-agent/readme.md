# 📄 Agente Inteligente de Incidentes con LLAMA - CrewAI - Streamlit  
Envía una PQR. El agente la comprende, clasifica, analiza sentimientos, la registra en Excel y notifica automáticamente al área responsable. Desde una interfaz web.

## 🚀 **¿Qué Hace?**
Un asistente inteligente que permite a los usuarios ingresar incidentes (PQRs) por medio de texto. Utiliza modelos LLM para comprender, categorizar y analizar cada mensaje. Guarda los datos en un Excel estructurado y notifica al área encargada.

## 🛠️ **Arquitectura**
- 🧠 **Clasificación y análisis**: Usa LLAMA-3 por medio de Groq para comprender la PQR.
- 😊 **Análisis de sentimientos**: Positivo, negativo o neutral.
- 📄 **Registro en Excel**: Guarda cada incidente con campos clave.
- 🤖 **Orquestación con CrewAI**: Agentes separados por rol y responsabilidad.
- 🌐 **Interfaz en Streamlit**: Sencilla e interactiva.

## 🧠 **Características Clave**
- Comprensión automática de incidentes con LLMs.
- Clasificación y asignación automática por área.
- Registro estructurado en Excel.

## 🧪 **Tecnologías Utilizadas**
- **LLM**: LLAMA-3
- **Frameworks**: CrewAI, Streamlit
- **Sentimientos**: LLAMA-3
- **Excel**: pandas, openpyxl

## 📊 **Estructura del Excel**
| Text | Category | Area | Sentimient | date |
|-------|-----------|------|-------------|-------|

**Desarrollado por [Yeins Aristizabal](https://www.linkedin.com/in/yeins-aristizabal/)**

🔗 [YouTube]
