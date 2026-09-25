import json
import os

from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage

from fact_checker.state import FactCheckState

_SYSTEM = """You are an evidence synthesizer. Given a claim, supporting evidence, and counter-evidence,
produce a balanced 3-5 sentence summary of what the evidence shows. Be neutral and objective.
Do not render a verdict — only summarize the evidence landscape."""


def synthesizer_node(state: FactCheckState) -> dict:
    llm = ChatBedrockConverse(
        model=os.environ["BEDROCK_MODEL_ID"],
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
    supporting = json.dumps(state["research_results"], ensure_ascii=False)
    counter = json.dumps(state["counter_evidence"], ensure_ascii=False)
    claim = state["parsed_claim"].get("checkable_query") or state["claim"]

    human_text = (
        f"Claim: {claim}\n\n"
        f"Supporting evidence:\n{supporting}\n\n"
        f"Counter-evidence:\n{counter}"
    )
    messages = [
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=human_text),
    ]
    response = llm.invoke(messages)
    return {"synthesis": response.content.strip()}
