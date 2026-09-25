import os

from fact_checker.state import FactCheckState
from fact_checker.tools.search import search_web


def researcher_node(state: FactCheckState) -> dict:
    query = state["parsed_claim"].get("checkable_query") or state["claim"]
    results = search_web(
        query=query,
        max_results=int(os.environ.get("RESEARCHER_MAX_RESULTS", "5")),
        api_key=os.environ.get("TAVILY_API_KEY"),
    )
    return {"research_results": results}
