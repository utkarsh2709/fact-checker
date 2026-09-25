from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from fact_checker.graph import compiled_graph
from fact_checker.models import VerdictResponse, VerifyRequest
from fact_checker.state import FactCheckState

load_dotenv()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Graph is compiled at import time via graph.py module level
    yield


app = FastAPI(title="Fact Checker API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/verify", response_model=VerdictResponse)
def verify_claim(request: VerifyRequest) -> VerdictResponse:
    initial_state: FactCheckState = {
        "claim": request.claim,
        "parsed_claim": {},
        "research_results": [],
        "counter_evidence": [],
        "synthesis": "",
        "verdict": "",
        "confidence": 0.0,
        "reasoning": "",
    }
    try:
        final_state = compiled_graph.invoke(initial_state)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return VerdictResponse(**final_state)
