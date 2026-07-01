from src.agents.jd_analyzer import analyze_jd
from src.agents.gap_analyzer import analyze_gap

sample_jd = """
We're hiring an AI Engineer with strong Python skills.
Must have hands-on experience with LLMs, RAG pipelines, and vector
databases like FAISS or ChromaDB. Familiarity with LangChain, FastAPI,
and prompt engineering is a big plus. Experience with Kubernetes and
AWS is required. 1-2 years of experience preferred.
"""

# Step 1: analyze the JD
jd = analyze_jd(sample_jd)
print("JD analyzed. Role:", jd.role_title)

# Step 2: compare against resume
gap = analyze_gap(jd)

print("\n" + "=" * 60)
print("GAP ANALYSIS")
print("=" * 60)
print("Matched skills :", gap.matched_skills)
print("Missing skills :", gap.missing_skills)
print("Partial skills :", gap.partial_skills)
print("Match score    :", gap.match_score, "/ 100")
print("Recommendation :", gap.recommendation)
