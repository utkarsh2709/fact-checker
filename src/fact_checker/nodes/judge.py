import os

from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage

from fact_checker.state import FactCheckState
from fact_checker.utils import parse_llm_json

_VALID_VERDICTS = {"TRUE", "FALSE", "MISLEADING", "UNVERIFIED"}

_SYSTEM = """You are a fact-checking judge. Given a claim and an evidence summary, render a final verdict.

Respond with ONLY a JSON object with these exact keys:
- "verdict": one of "TRUE", "FALSE", "MISLEADING", or "UNVERIFIED"
- "confidence": a float between 0.0 and 1.0 representing your certainty
- "reasoning": 2-3 sentences explaining your verdict

Use "UNVERIFIED" when evidence is insufficient or contradictory."""


def judge_node(state: FactCheckState) -> dict:
    llm = ChatBedrockConverse(
        model=os.environ["BEDROCK_MODEL_ID"],
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
    human_text = (
        f"Claim: {state['claim']}\n\n"
        f"Evidence summary:\n{state['synthesis']}"
    )
    messages = [
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=human_text),
    ]
    response = llm.invoke(messages)
    result = parse_llm_json(response.content)

    verdict = result.get("verdict", "UNVERIFIED").upper()
    if verdict not in _VALID_VERDICTS:
        raise ValueError(f"Invalid verdict from LLM: {verdict!r}. Must be one of {_VALID_VERDICTS}.")

    return {
        "verdict": verdict,
        "confidence": float(result.get("confidence", 0.5)),
        "reasoning": result.get("reasoning", ""),
    }
