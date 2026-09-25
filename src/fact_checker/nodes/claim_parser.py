import os

from langchain_aws import ChatBedrockConverse
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
    llm = ChatBedrockConverse(
        model=os.environ["BEDROCK_MODEL_ID"],
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
    messages = [
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=f"Claim: {state['claim']}"),
    ]
    response = llm.invoke(messages)
    parsed = parse_llm_json(response.content)
    return {"parsed_claim": parsed}
