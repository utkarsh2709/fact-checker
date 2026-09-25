from typing import TypedDict


class FactCheckState(TypedDict):
    claim: str
    parsed_claim: dict
    research_results: list[dict]
    counter_evidence: list[dict]
    synthesis: str
    verdict: str
    confidence: float
    reasoning: str
