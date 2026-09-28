import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from fact_checker.state import FactCheckState
from fact_checker.tools.search import search_web

_SYSTEM = """You are an adversarial fact-checker. Generate a concise search query that would find evidence
AGAINST or CONTRADICTING the given claim. Return ONLY the search query string, nothing else."""


def adversarial_node(state: FactCheckState) -> dict:
    llm = ChatGoogleGenerativeAI(
        model=os.environ.get("GEMINI_MODEL_ID", "gemini-2.0-flash"),
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
    )
    claim_text = state["parsed_claim"].get("checkable_query") or state["claim"]
    messages = [
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=f"Claim: {claim_text}"),
    ]
    response = llm.invoke(messages)
    counter_query = response.content.strip().strip('"')

    results = search_web(
        query=counter_query,
        max_results=int(os.environ.get("RESEARCHER_MAX_RESULTS", "5")),
        api_key=os.environ.get("TAVILY_API_KEY"),
    )
    return {"counter_evidence": results}
