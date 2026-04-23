
# 🧠 Agentic RAG System (LangGraph + FastAPI + Docker)

An end-to-end **Agentic Retrieval-Augmented Generation (RAG)** system built using:

- LangGraph (agent orchestration)
- FastAPI (API layer)
- ChromaDB (vector store)
- Ollama (local LLM inference)
- Docker + GitHub Actions (CI/CD pipeline)

This project demonstrates how to build a production-style LLM system with modular components, observability, and deployment readiness.

---

## 🚀 Features

- Agentic Workflow (LangGraph)
  - Router → RAG Node → Final Node
- Context-Aware Query Rewriting
- Vector Retrieval with ChromaDB
- Traceable Execution Flow
- FastAPI-based API
- Dockerized Deployment
- CI/CD with GitHub Actions
- Docker Hub Auto Publish

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
   ↓
Final Answer + Trace

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
- Dependency installation
- Syntax checks
- Pytest execution

CD (Docker):
- Build Docker image
- Push to Docker Hub
- Tagging: latest, main, v*

---

## 📌 Key Concepts Demonstrated

- Agentic orchestration with LangGraph
- Retrieval-Augmented Generation (RAG)
- Vector similarity search (ChromaDB)
- Query rewriting for better retrieval
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

- Streaming responses
- Multi-agent routing
- Tool usage (web/API integration)
- Observability dashboard
- Cloud deployment (Render / Azure)

---

## 👤 Author

Deepak L  
MSc Mechatronics | ML | Computer Vision | MLOps

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to fork!



