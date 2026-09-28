from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from fact_checker.api import app

client = TestClient(app)

_FULL_STATE = {
    "claim": "The Great Wall of China is visible from space.",
    "parsed_claim": {"checkable_query": "great wall china visible space"},
    "research_results": [{"url": "https://example.com", "title": "Test", "content": "..."}],
    "counter_evidence": [],
    "synthesis": "Evidence suggests the claim is false.",
    "verdict": "FALSE",
    "confidence": 0.9,
    "reasoning": "The Great Wall is too narrow to be seen from space with the naked eye.",
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_verify_returns_verdict():
    mock_graph = MagicMock()
    mock_graph.invoke.return_value = _FULL_STATE

    # Patch the name in the api module's namespace directly
    with patch("fact_checker.api.compiled_graph", mock_graph):
        response = client.post(
            "/verify",
            json={"claim": "The Great Wall of China is visible from space."},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "FALSE"
    assert data["confidence"] == 0.9
    assert "reasoning" in data


def test_verify_rejects_short_claim():
    response = client.post("/verify", json={"claim": "Hi"})
    assert response.status_code == 422


def test_verify_rejects_missing_claim():
    response = client.post("/verify", json={})
    assert response.status_code == 422
