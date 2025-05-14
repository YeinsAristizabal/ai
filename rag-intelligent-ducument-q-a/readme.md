# Intelligent Document Q&A App with Streamlit  
Ask questions. Get instant answers. All from your documents — powered by open-source AI.

## 🚀 **What It Does**
An intelligent assistant that lets users upload PDFs and ask questions in natural language. Built with open-source LLMs, LangChain, FAISS, and Streamlit — 100% local, secure, and blazing fast.

## 🧠 **Why It Matters**
Businesses spend hours searching internal files like contracts, invoices, or medical reports. This tool automates that, turning documents into a searchable AI assistant — no cloud, no privacy risk.

## 🛠️ **Architecture**
🗂️ PDF Parsing: Extracts text from PDFs.
✂️ Chunking: Splits into sections for accurate retrieval.
🔍 Semantic Search: Uses FAISS & embeddings to find relevant parts.
🧠 Local LLM (Ollama): Generates answers based on the document.
🌐 Wikipedia Tool: Fallback when documents lack context.
🔁 LangChain: Orchestrates the multi-step reasoning flow.
📊 Streamlit: Provides clean, interactive web UI.

## 🧠 Key Features
- Ask questions in natural language using local open-source LLMs.
- Instant answers from internal company documents.
- Wikipedia integration for external knowledge.
- 100% local, secure, and private — no data leaves your machine.

## 🧪 **Tech Stack**
- **LLM**: gemma:2b via Ollama
- **Vector DB**: FAISS
- **Frameworks**: LangChain, Streamlit
- **Embeddings**: sentence-transformers
- **Parsing**: PyPDFLoader
- **Language Detection**: 

**Developed by [Yeins Aristizabal](https://www.linkedin.com/in/yeins-aristizabal/)**  
🔗 [GitHub](https://github.com/YeinsAristizabal/ai/tree/main/streamlit-dashboard-customer-segmentation)