from src.agents.jd_analyzer import analyze_jd
from src.agents.gap_analyzer import analyze_gap
from src.agents.tailoring import tailor_application
from src.agents.critic import review_content
from src.tools.ats_scorer import compare_ats
from src.rag.ingest import extract_pdf_text

sample_jd = """
We're hiring an AI Engineer with strong Python skills.
Must have hands-on experience with LLMs, RAG pipelines, and vector
databases like FAISS or ChromaDB. Familiarity with LangChain, FastAPI,
and prompt engineering is a big plus. 1-2 years of experience preferred.
"""

# Full chain
jd = analyze_jd(sample_jd)
print("1. JD analyzed:", jd.role_title)

gap = analyze_gap(jd)
print("2. Gap analyzed. Match score:", gap.match_score)

tailored = tailor_application(jd, gap)
print("3. Content tailored.")

# --- Critic review ---
review = review_content(tailored)
print("\n" + "=" * 60)
print("CRITIC REVIEW")
print("=" * 60)
print("Truthful  :", review.is_truthful)
print("Verdict   :", review.verdict)
print("Fabricated:", review.fabricated_claims)
print("Exaggerated:", review.exaggerations)
print("Feedback  :", review.feedback)

# --- ATS score ---
original_resume = extract_pdf_text("data/master_resume.pdf")
ats = compare_ats(jd, original_resume, tailored)
print("\n" + "=" * 60)
print("ATS SCORE")
print("=" * 60)
print(f"Tailored content JD-fit : {ats['tailored_score']}%")
print(f"(Full resume coverage)  : {ats['resume_score']}%")
print(f"Keywords matched        : {ats['matched']}")
print(f"Still missing           : {ats['still_missing']}")
print(f"Total JD keywords       : {ats['total_keywords']}")
