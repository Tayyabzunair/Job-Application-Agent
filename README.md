# 🤖 Autonomous Job-Application Agent

An agentic AI system that analyzes job descriptions, tailors resumes & cover letters
using RAG over your profile, checks for factual accuracy, and tracks applications —
all with a human-in-the-loop approval step.

## ✨ Features

- **JD Analyzer** — Extracts skills, seniority & ATS keywords from any job description
- **RAG-Powered Tailoring** — Retrieves relevant experience from your profile (ChromaDB)
- **Gap Analysis** — Matches your skills against job requirements
- **Critic Agent** — Verifies tailored content has no fabricated claims
- **ATS Scorer** — Measures keyword-match improvement (before vs after)
- **Human-in-the-loop** — You approve before anything is finalized
- **Application Tracker** — Logs applications automatically

## 🛠️ Tech Stack

- **Orchestration:** LangGraph
- **LLM:** Groq (Llama 3.3 70B)
- **RAG / Vector DB:** ChromaDB
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Observability:** LangSmith

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Tayyabzunair/job-application-agent.git
cd job-application-agent
