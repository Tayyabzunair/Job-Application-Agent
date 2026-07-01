from src.agents.jd_analyzer import analyze_jd
from src.agents.gap_analyzer import analyze_gap
from src.agents.tailoring import tailor_application

sample_jd = """
We're hiring an AI Engineer with strong Python skills.
Must have hands-on experience with LLMs, RAG pipelines, and vector
databases like FAISS or ChromaDB. Familiarity with LangChain, FastAPI,
and prompt engineering is a big plus. 1-2 years of experience preferred.
"""

# Run the chain: JD -> Gap -> Tailoring
jd = analyze_jd(sample_jd)
print("JD analyzed. Role:", jd.role_title)

gap = analyze_gap(jd)
print("Gap analyzed. Match score:", gap.match_score)

tailored = tailor_application(jd, gap)

print("\n" + "=" * 60)
print("TAILORED RESUME BULLETS")
print("=" * 60)
for b in tailored.tailored_bullets:
    print(" -", b)

print("\n" + "=" * 60)
print("PROFESSIONAL SUMMARY")
print("=" * 60)
print(tailored.professional_summary)

print("\n" + "=" * 60)
print("COVER LETTER")
print("=" * 60)
print(tailored.cover_letter)

print("\n" + "=" * 60)
print("KEYWORDS USED:", tailored.keywords_used)
