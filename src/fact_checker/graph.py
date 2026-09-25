from langgraph.graph import END, StateGraph

from fact_checker.nodes import (
    adversarial_node,
    claim_parser_node,
    judge_node,
    researcher_node,
    synthesizer_node,
)
from fact_checker.state import FactCheckState


def build_graph():
    graph = StateGraph(FactCheckState)

    graph.add_node("claim_parser", claim_parser_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("adversarial_verifier", adversarial_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.add_node("judge", judge_node)

    graph.set_entry_point("claim_parser")

    # Fan out: researcher and adversarial_verifier run in parallel
    graph.add_edge("claim_parser", "researcher")
    graph.add_edge("claim_parser", "adversarial_verifier")

    # Both converge at synthesizer; LangGraph waits for all incoming edges
    graph.add_edge("researcher", "synthesizer")
    graph.add_edge("adversarial_verifier", "synthesizer")

    graph.add_edge("synthesizer", "judge")
    graph.add_edge("judge", END)

    return graph.compile()


compiled_graph = build_graph()
