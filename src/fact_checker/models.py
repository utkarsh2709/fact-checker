from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    claim: str = Field(..., min_length=5, max_length=2000)


class VerdictResponse(BaseModel):
    claim: str
    verdict: str
    confidence: float
    reasoning: str
    synthesis: str
    research_results: list[dict]
    counter_evidence: list[dict]
