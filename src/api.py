"""
FastAPI backend for the Job Application Agent.
Exposes endpoints to analyze a JD (runs the agentic graph) and to
approve the tailored result (human-in-the-loop).
"""
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.tools.tracker import log_application, get_all_applications
from src.graph import app_graph
from src.tools.job_fetcher import fetch_jobs

app = FastAPI(title="Job Application Agent API")

# In-memory store for analysis results (Phase 1 MVP).
# key = result_id, value = analysis data. Replace with a DB later.
RESULTS_STORE: dict[str, dict] = {}


# ---------- Request models ----------

class AnalyzeRequest(BaseModel):
    jd_text: str


class ApproveRequest(BaseModel):
    result_id: str
    # Optional edited content from the user (human-in-the-loop)
    edited_bullets: list[str] | None = None
    edited_cover_letter: str | None = None


# ---------- Endpoints ----------

@app.get("/")
def health():
    return {"status": "ok", "service": "Job Application Agent"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Runs the full agentic graph on a job description."""
    if not req.jd_text.strip():
        raise HTTPException(status_code=400, detail="jd_text cannot be empty")

    initial_state = {"jd_text": req.jd_text, "retry_count": 0}
    final_state = app_graph.invoke(initial_state)

    # Build a clean response
    result_id = str(uuid.uuid4())[:8]
    result = {
        "result_id": result_id,
        "role": final_state["jd"].role_title,
        "seniority": final_state["jd"].seniority,
        "match_score": final_state["gap"].match_score,
        "matched_skills": final_state["gap"].matched_skills,
        "missing_skills": final_state["gap"].missing_skills,
        "tailored_bullets": final_state["tailored"].tailored_bullets,
        "professional_summary": final_state["tailored"].professional_summary,
        "cover_letter": final_state["tailored"].cover_letter,
        "critic_verdict": final_state["review"].verdict,
        "is_truthful": final_state["review"].is_truthful,
        "fabricated_claims": final_state["review"].fabricated_claims,
        "ats_score": final_state["ats"]["tailored_score"],
        "ats_matched": final_state["ats"]["matched"],
        "ats_missing": final_state["ats"]["still_missing"],
        "approved": False,
    }

    # Store it so it can be approved later
    RESULTS_STORE[result_id] = result
    return result


@app.post("/approve")
def approve(req: ApproveRequest):
    """Human-in-the-loop: approve (and optionally edit) a tailored result."""
    result = RESULTS_STORE.get(req.result_id)
    if not result:
        raise HTTPException(status_code=404, detail="result_id not found")

    # Apply user edits if provided
    if req.edited_bullets is not None:
        result["tailored_bullets"] = req.edited_bullets
    if req.edited_cover_letter is not None:
        result["cover_letter"] = req.edited_cover_letter

    result["approved"] = True

     # Log the approved application to the tracker (persists to disk)
    logged = log_application(result)

    return {"message": "Approved and logged.", "logged": logged, "result": result}

@app.get("/results")
def list_results():
    """Returns all analyzed results (for a future dashboard)."""
    return list(RESULTS_STORE.values())
@app.get("/applications")
def applications():
    """Returns all approved/tracked applications from the tracker."""
    return get_all_applications()
@app.get("/jobs")
def jobs(search: str = "ai engineer", limit: int = 5):
    """
    Fetches live remote jobs from RemoteOK.
    Example: /jobs?search=machine learning&limit=5
    """
    return fetch_jobs(search=search, limit=limit)
class AnalyzeJobRequest(BaseModel):
    job_description: str


@app.post("/analyze-job")
def analyze_job(req: AnalyzeJobRequest):
    """
    Convenience endpoint: analyze a fetched job's description directly.
    (Same as /analyze but named for the job-fetch flow.)
    """
    return analyze(AnalyzeRequest(jd_text=req.job_description))
