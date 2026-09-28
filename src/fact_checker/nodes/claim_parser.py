import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from fact_checker.state import FactCheckState
from fact_checker.utils import parse_llm_json

_SYSTEM = """You are a claim analysis assistant. Given a claim, extract a structured JSON object with these exact keys:
- "subject": who or what the claim is about
- "predicate": what is being asserted about the subject
- "context": any time, location, or qualifying conditions mentioned
- "checkable_query": a concise, search-engine-ready query to verify this claim

Respond with ONLY the JSON object, no other text."""


def claim_parser_node(state: FactCheckState) -> dict:
    llm = ChatGoogleGenerativeAI(
        model=os.environ.get("GEMINI_MODEL_ID", "gemini-2.0-flash"),
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
    )
    messages = [
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=f"Claim: {state['claim']}"),
    ]
    response = llm.invoke(messages)
    parsed = parse_llm_json(response.content)
    return {"parsed_claim": parsed}
