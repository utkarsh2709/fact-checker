from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with patch("fact_checker.graph.build_graph") as mock_build:
        mock_graph = MagicMock()
        mock_build.return_value = mock_graph
        # Re-import api after patching so compiled_graph uses the mock
        import importlib

        import fact_checker.graph as g
        g.compiled_graph = mock_graph

        from fact_checker.api import app
        return TestClient(app), mock_graph


def test_health(client):
    tc, _ = client
    response = tc.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_verify_returns_verdict(client):
    tc, mock_graph = client
    mock_graph.invoke.return_value = {
        "claim": "The Great Wall of China is visible from space.",
        "parsed_claim": {"checkable_query": "great wall china visible space"},
        "research_results": [{"url": "https://example.com", "title": "Test", "content": "..."}],
        "counter_evidence": [],
        "synthesis": "Evidence suggests the claim is false.",
        "verdict": "FALSE",
        "confidence": 0.9,
        "reasoning": "The Great Wall is too narrow to be seen from space with the naked eye.",
    }
    response = tc.post("/verify", json={"claim": "The Great Wall of China is visible from space."})
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "FALSE"
    assert data["confidence"] == 0.9
    assert "reasoning" in data


def test_verify_rejects_short_claim(client):
    tc, _ = client
    response = tc.post("/verify", json={"claim": "Hi"})
    assert response.status_code == 422


def test_verify_rejects_missing_claim(client):
    tc, _ = client
    response = tc.post("/verify", json={})
    assert response.status_code == 422
