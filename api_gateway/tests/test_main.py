import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from src.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "RAG Commercial Analytics API"}

@patch('src.main.app.state.rag_service')
@patch('src.main.app.state.guardrails_service')
def test_process_query_success(mock_guardrails, mock_rag):
    """Test successful query processing"""
    # Mock guardrails
    mock_guardrails.sanitize_input.return_value = "test query"
    mock_guardrails.check_relevance.return_value = True
    mock_guardrails.validate_output.return_value = "test response"
    
    # Mock RAG service
    mock_rag.process_query.return_value = {
        "response": "test response",
        "sources": [],
        "confidence": 0.8
    }
    
    # Test request
    response = client.post("/query", json={"query": "test query"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "test query"
    assert data["response"] == "test response"
    assert data["confidence"] == 0.8

@patch('src.main.app.state.guardrails_service')
def test_process_query_irrelevant(mock_guardrails):
    """Test query rejection for irrelevant content"""
    mock_guardrails.sanitize_input.return_value = "irrelevant query"
    mock_guardrails.check_relevance.return_value = False
    
    response = client.post("/query", json={"query": "irrelevant query"})
    
    assert response.status_code == 400
    assert "not relevant" in response.json()["detail"]

@patch('src.main.app.state.rag_service')
def test_ingest_documents_success(mock_rag):
    """Test successful document ingestion"""
    mock_rag.ingest_documents.return_value = 5
    
    test_documents = [
        {
            "id": "doc1",
            "content": "test content",
            "source": "test_source",
            "type": "document"
        }
    ]
    
    response = client.post("/documents/ingest", json={"documents": test_documents})
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["processed"] == 5

@patch('src.main.app.state.redis_client')
def test_get_metrics(mock_redis):
    """Test metrics endpoint"""
    mock_redis.get.side_effect = lambda key: {"total_queries": "100", "successful_queries": "95"}.get(key, 0)
    
    response = client.get("/metrics")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_queries"] == 100
    assert data["successful_queries"] == 95
    assert data["success_rate"] == 0.95

def test_query_validation():
    """Test query validation"""
    # Test empty query
    response = client.post("/query", json={})
    assert response.status_code == 422  # Validation error
    
    # Test invalid JSON
    response = client.post("/query", json={"query": ""})
    # Should pass validation but might fail in processing