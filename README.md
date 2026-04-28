
![CI](https://github.com/DeepuLIN/llm-rag-system/actions/workflows/ci.yml/badge.svg)
![Docker](https://github.com/DeepuLIN/llm-rag-system/actions/workflows/docker.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

# 🧠 Agentic RAG System (LangGraph + FastAPI + Docker)

An end-to-end Agentic Retrieval-Augmented Generation (RAG) system built with a modular, production-oriented architecture.

This project demonstrates how to design, orchestrate, and deploy an LLM-powered system with intelligent routing, query rewriting, and traceable execution.

---

## 🚀 Features

- Agentic RAG Workflow (LangGraph)  
  Structured pipeline: Router → Query Rewrite → Retrieval → Answer Generation

- Intelligent Query Routing  
  Dynamically determines whether retrieval is required

- Context-Aware Query Rewriting  
  Improves retrieval accuracy for ambiguous or incomplete queries

- Vector Search with ChromaDB  
  Semantic retrieval over a custom knowledge base

- Traceable Execution Flow  
  End-to-end visibility into each step of the pipeline

- FastAPI Backend  
  Production-ready API for integration

- Gradio Interface  
  Interactive UI for testing and demonstration

- Dockerized Deployment  
  Reproducible and portable environment

- CI/CD with GitHub Actions  
  Automated testing and build pipeline

- Docker Hub Auto Publish  
  Continuous container build and deployment

---

## 🏗️ Architecture

User Query

   ↓
   
FastAPI (/ask)

   ↓
   
LangGraph Agent

   ↓

   
[Query Rewrite]

   ↓
   
[Retriever → ChromaDB]

   ↓
   
[LLM (Ollama)]

=======
Router
   ↓
Query Rewriter (if needed)
   ↓
Retriever (ChromaDB)
   ↓
LLM (Ollama)

   ↓
   
Final Answer + Trace

---

## 💡 Why Agentic RAG?

Traditional RAG systems often fail when:
- queries are vague or underspecified
- retrieval misses relevant context
- no adaptive mechanism exists

This system improves reliability by:
- rewriting queries before retrieval
- dynamically routing requests
- structuring reasoning using a graph-based workflow

---

## 🧪 Example

Query: Who is the CEO of InsureLLM?

→ Rewritten Query: Who is the CEO of Insure LLM company?
→ Retrieved Sources: employees/avery_lancaster.md
→ Answer: Avery Lancaster is the CEO of InsureLLM.

---

## 📂 Project Structure

src/

├── api/            # FastAPI app

├── graph/          # LangGraph definition

├── nodes/          # Agent nodes (rag, router, final)

├── rag/            # RAG pipeline (retriever, vectorstore)


data/

└── knowledge-base/ # Markdown knowledge base


vector_db/          # ChromaDB (local, not committed)


.github/

└── workflows/      # CI/CD pipelines

Dockerfile

docker-compose.yml

---

## 🧪 API Usage

Health Check:
curl http://localhost:8000/health

Ask a Question:
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who is Maxine Thompson?",
    "history": []
  }'

---

## 🐳 Run with Docker

Pull Image:
docker pull deepulin/llm-rag-api:latest

Run Container:
docker run --rm --network host \
  -v "$(pwd)/vector_db:/app/vector_db" \
  deepulin/llm-rag-api:latest

---

## ⚙️ Local Setup

git clone https://github.com/DeepuLIN/llm-rag-system.git
cd llm-rag-system

pip install -r requirements.txt

# Build vector DB
python -m src.rag.vectorstore

# Run API
uvicorn src.api.api:app --reload

---

## 🔄 CI/CD Pipeline

CI (GitHub Actions):
- dependency installation
- syntax checks
- pytest execution

CD (Docker):
- build Docker image
- push to Docker Hub
- tagging: latest, main, v*

---

## 📌 Key Concepts Demonstrated

- Agentic orchestration with LangGraph
- Retrieval-Augmented Generation (RAG)
- Vector similarity search (ChromaDB)
- Query rewriting for improved retrieval
- Modular LLM system design
- Dockerized ML deployment
- CI/CD for ML systems

---

## ⚠️ Notes

- vector_db/ is mounted at runtime (not committed)
- Requires local Ollama running on port 11434
- Uses CPU-based embeddings for portability

---

## 🔮 Future Improvements

- streaming responses
- multi-agent routing
- tool usage (web/API integration)
- observability dashboard
- cloud deployment (Render / Azure)

---

## 👤 Author

Deepak L  
ML | Computer Vision | MLOps

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to fork!
