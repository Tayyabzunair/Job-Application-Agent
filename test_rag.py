from src.rag.retriever import retrieve_relevant

# Test — RAG, LLM se related experience khojo
query = "RAG, LLM, vector database experience"
results = retrieve_relevant(query, k=3)

print(f"\n🔍 Query: {query}\n")
print("=" * 60)
for i, chunk in enumerate(results, 1):
    print(f"\n[Match {i}]")
    print(chunk)
    print("-" * 60)
