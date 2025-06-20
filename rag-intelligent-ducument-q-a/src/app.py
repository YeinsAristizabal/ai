# app.py
import streamlit as st
import tempfile
from langdetect import detect, DetectorFactory
from components import load_llm, process_pdf
from prompt import CUSTOM_PROMPT
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
import base64

# Setup
st.set_page_config(page_title="Document Assistant")
st.title("📄 Intelligent Document Q&A ChatBot App (100% Open Source - RAG")
st.subheader("LangChain - OLLAMA - GEMMA - FAISS- Streamlit")
st.markdown("Upload a document and ask questions in natural language.")
st.markdown("---")

columns = st.columns((1, 1, 1))
with columns[0]:
    st.page_link('https://www.linkedin.com/in/yeins-aristizabal/', label="LinkedIn")
with columns[1]:
    st.page_link('https://github.com/YeinsAristizabal/ai/tree/main/streamlit-dashboard-customer-segmentation', label="GitHub")
with columns[2]:
    st.markdown("**Developed by Yeins Aristizabal**")

st.markdown("---")

# Session State Setup
# inicializa variables en el estado de sesión de Streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "language" not in st.session_state:
    st.session_state.language = ""

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file and "pdf_bytes" not in st.session_state:
    pdf_bytes = uploaded_file.read()
    st.session_state["pdf_bytes"] = pdf_bytes
    st.session_state["filename"] = uploaded_file.name

# Sidebar: Metadata and Tool Info
with st.sidebar:
    st.markdown("### 📄 Document Info")
    if st.session_state.pdf_loaded:
        st.markdown(f"**Filename:** `{st.session_state.filename}`")
        st.markdown(f"**Detected language:** `{st.session_state.language}`")

    st.markdown("---")
    st.markdown("### 📄 PDF Preview")
    if "pdf_bytes" in st.session_state:
        # Mostrar vista previa del PDF desde bytes guardados
        # Convierte un PDF en bytes a base64
        base64_pdf = base64.b64encode(st.session_state["pdf_bytes"]).decode('utf-8')
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ℹ️ About this app")
    st.markdown(
        """
        - **Open Source Chat + Document Assistant**
        - Built with: 
            - `LangChain`
            - `Streamlit`
            - `FAISS`
            - `Open-Source LLMs - Ollama: Gemma 2b`
        - Features:
            - Document Q&A
            - Summary with Memory
            - Language Detection
            - RAG documents
        """
    )

# Button to trigger document analysis
button_analyze = st.button("Analyze", type="primary")

if "pdf_bytes" in st.session_state and not st.session_state.pdf_loaded and button_analyze:
    with st.spinner("Processing document..."):
        # Crea un archivo PDF temporal con el contenido en bytes almacenado en la sesión y guarda su ruta en pdf_path.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(st.session_state["pdf_bytes"])
            pdf_path = tmp_file.name

        # Extract text for language detection and preview
        reader = PdfReader(pdf_path)
        raw_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        st.session_state.pdf_text = raw_text

        # Language detection
        DetectorFactory.seed = 0
        try:
            detected_lang = detect(raw_text[:1000])
        except:
            detected_lang = "unknown"
        st.session_state.language = detected_lang

        # Load LLM and retriever
        llm = load_llm()
        retriever = process_pdf(pdf_path)

        # Get summary
        summary = llm.predict(f"Resume el ducumento en 3 puntos:\n{raw_text[:3000]}")
        st.session_state.summary = summary

        # Setup memory and prompt
        memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
        prompt = PromptTemplate(
            input_variables=["chat_history", "question", "context"],
            template=CUSTOM_PROMPT
        )

        # Build Conversational QA chain
        st.session_state.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, # gemma
            retriever=retriever, # context
            memory=memory, # chat history
            combine_docs_chain_kwargs={"prompt": prompt},
            verbose=True
        )
        st.session_state.pdf_loaded = True

# Show summary only if document was analyzed
if st.session_state.pdf_loaded:
    if st.button("📌 Show Document Summary"):
        st.markdown("### 🔍 Summary")
        st.markdown(st.session_state.summary)

# Chat interface
if st.session_state.qa_chain:
    user_input = st.chat_input("Say something or ask a question...")
    if user_input:
        with st.spinner("Thinking..."):
            response = st.session_state.qa_chain.run(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])