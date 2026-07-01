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

2. Create virtual environment

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

3. Install dependencies
pip install -r requirements.txt

4. Set up environment variables
Create a .env file:

GROQ_API_KEY=your_groq_key_here
LANGCHAIN_TRACING_V2=false

5. Run
python test_jd.py

📌 Status
🚧 Under active development — Phase 1 (MVP)

 JD Analyzer Agent
 RAG setup (resume knowledge base)
 Gap Analyzer
 Tailoring Agent
 Critic Agent + ATS Scorer
 Streamlit UI + Tracker
👤 Author
Muhammad Tayyab Zunair — AI Engineer 