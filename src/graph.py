"""
LangGraph orchestration.
Connects all agents into a stateful graph with a self-correction loop:
if the Critic rejects the tailored content, it loops back to re-tailor.
"""
from langgraph.graph import StateGraph, START, END

from src.schemas import AgentState
from src.agents.jd_analyzer import analyze_jd
from src.agents.gap_analyzer import analyze_gap
from src.agents.tailoring import tailor_application
from src.agents.critic import review_content
from src.tools.ats_scorer import compare_ats
from src.rag.ingest import extract_pdf_text

MAX_RETRIES = 2  # how many times to re-tailor if the critic rejects


# ---------- NODES (each takes state, returns updated fields) ----------

def node_jd_analyzer(state: AgentState) -> dict:
    print("  [Node] JD Analyzer running...")
    jd = analyze_jd(state["jd_text"])
    return {"jd": jd}


def node_gap_analyzer(state: AgentState) -> dict:
    print("  [Node] Gap Analyzer running...")
    gap = analyze_gap(state["jd"])
    return {"gap": gap}


def node_tailoring(state: AgentState) -> dict:
    print("  [Node] Tailoring Agent running...")
    tailored = tailor_application(state["jd"], state["gap"])
    # increment retry counter each time we tailor
    return {"tailored": tailored, "retry_count": state.get("retry_count", 0) + 1}


def node_critic(state: AgentState) -> dict:
    print("  [Node] Critic Agent reviewing...")
    review = review_content(state["tailored"])
    return {"review": review}


def node_ats(state: AgentState) -> dict:
    print("  [Node] ATS Scorer running...")
    original_resume = extract_pdf_text("data/master_resume.pdf")
    ats = compare_ats(state["jd"], original_resume, state["tailored"])
    return {"ats": ats}


# ---------- CONDITIONAL EDGE (the decision-maker) ----------

def route_after_critic(state: AgentState) -> str:
    """
    Decides what to do after the Critic reviews the content.
    - If approved (truthful), proceed to ATS scoring.
    - If rejected but retries remain, loop back to re-tailor.
    - If out of retries, proceed anyway (best effort).
    """
    review = state["review"]
    retries = state.get("retry_count", 0)

    if review.is_truthful:
        print("  [Route] Critic APPROVED -> ATS scoring")
        return "approved"

    if retries < MAX_RETRIES:
        print(f"  [Route] Critic flagged issues -> re-tailoring (attempt {retries + 1})")
        return "retry"

    print("  [Route] Max retries reached -> proceeding anyway")
    return "approved"


# ---------- BUILD THE GRAPH ----------

def build_graph():
    workflow = StateGraph(AgentState)

    # register nodes
    workflow.add_node("jd_analyzer", node_jd_analyzer)
    workflow.add_node("gap_analyzer", node_gap_analyzer)
    workflow.add_node("tailoring", node_tailoring)
    workflow.add_node("critic", node_critic)
    workflow.add_node("ats", node_ats)

    # linear edges
    workflow.add_edge(START, "jd_analyzer")
    workflow.add_edge("jd_analyzer", "gap_analyzer")
    workflow.add_edge("gap_analyzer", "tailoring")
    workflow.add_edge("tailoring", "critic")

    # conditional edge after critic (self-correction loop)
    workflow.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "approved": "ats",       # good -> score it
            "retry": "tailoring",    # bad -> tailor again
        },
    )

    # end
    workflow.add_edge("ats", END)

    return workflow.compile()


# compiled graph, importable elsewhere
app_graph = build_graph()
