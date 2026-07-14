# RAG in LangGraph - Day 8

**RAG-Enabled LLM with Tool Calling using LangGraph**

## 📌 Overview

This project demonstrates how to build a **Retrieval-Augmented Generation (RAG)** pipeline integrated with LangGraph's tool calling pattern. The LLM can query private PDF documents using a custom tool, making it perfect for document-based Q&A systems.

**Key distinction:** This is an **LLM with tool calling** (not a fully autonomous agent) - the LLM decides when to call the `rag_tool` based on the user's query.

## ✨ Features

- **📄 PDF Ingestion**: Load documents using `PyPDFLoader`
- **✂️ Text Chunking**: Split documents with `RecursiveCharacterTextSplitter`
- **🧠 Local Embeddings**: Generate embeddings using `Ollama` with `bge-m3:567m`
- **🗄️ Vector Storage**: Store embeddings in `ChromaDB` with persistence
- **🔍 Semantic Retrieval**: Retrieve top-k relevant chunks (k=5)
- **🛠️ Custom Tool**: `rag_tool` for document retrieval
- **🔄 Conditional Routing**: LLM automatically decides when to use the tool
- **🤖 Google Gemini**: Powered by Gemini 3.1 Flash Lite

## 🛠️ Tech Stack

- **LangGraph** - Workflow orchestration
- **LangChain** - LLM and tool integration
- **Google Gemini** - LLM provider
- **Ollama** - Local embeddings (bge-m3:567m)
- **ChromaDB** - Vector database
- **Python 3.13+**
