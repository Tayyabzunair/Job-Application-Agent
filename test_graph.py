from src.graph import app_graph

sample_jd = """
We're hiring an AI Engineer with strong Python skills.
Must have hands-on experience with LLMs, RAG pipelines, and vector
databases like FAISS or ChromaDB. Familiarity with LangChain, FastAPI,
and prompt engineering is a big plus. 1-2 years of experience preferred.
"""

# initial state
initial_state = {
    "jd_text": sample_jd,
    "retry_count": 0,
}

print("Running the agentic graph...\n")
final_state = app_graph.invoke(initial_state)

print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)
print("Role         :", final_state["jd"].role_title)
print("Match score  :", final_state["gap"].match_score)
print("Critic verdict:", final_state["review"].verdict)
print("Truthful     :", final_state["review"].is_truthful)
print("ATS JD-fit   :", final_state["ats"]["tailored_score"], "%")
print("\nTailored bullets:")
for b in final_state["tailored"].tailored_bullets:
    print("  -", b)
