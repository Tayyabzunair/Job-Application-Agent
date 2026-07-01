from src.agents.jd_analyzer import analyze_jd

sample_jd = """
We're hiring an AI Engineer with strong Python skills.
Must have hands-on experience with LLMs, RAG pipelines, and vector
databases like FAISS or ChromaDB. Familiarity with LangChain, FastAPI,
and prompt engineering is a big plus. 1-2 years of experience preferred.
Knowledge of Docker and cloud deployment is nice to have.
"""

result = analyze_jd(sample_jd)

print("Role:", result.role_title)
print("Seniority:", result.seniority)
print("Must-have:", result.must_have_skills)
print("Nice-to-have:", result.nice_to_have_skills)
print("ATS keywords:", result.key_ats_keywords)
print("Summary:", result.summary)
