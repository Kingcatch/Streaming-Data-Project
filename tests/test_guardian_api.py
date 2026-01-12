import os
import requests
import pytest
from src.guardian_api import fetch_guardian_articles

GUARDIAN_URL = "https://content.guardianapis.com/search"

@pytest.fixture
def mock_api_key(monkeypatch):
    monkeypatch.setenv("GUARDIAN_API_KEY", "test_api_key")
    
def test_fetch_articles_success(mock_api_key, requests_mock):
    mock_response = {
        "response": {
            "results": [{"id": "1"}, {"id": "2"}]
        }
    }
    
    requests_mock.get(GUARDIAN_URL, json=mock_response, status_code=200)
    
    articles = fetch_guardian_articles("technology")
    
    assert isinstance(articles, list)
    assert len(articles) == 2
    
def test_http_error_raises_exception(mock_api_key, requests_mock):
    requests_mock.get(GUARDIAN_URL, status_code=401)
    
    with pytest.raises(requests.exceptions.HTTPError):
        fetch_guardian_articles("technology")

def test_from_date_parameter(mock_api_key, requests_mock):
    requests_mock.get(GUARDIAN_URL, json={"response": {"results": []}}, status_code=200)
    
    articles = fetch_guardian_articles("science", from_date=None)
    assert articles == []