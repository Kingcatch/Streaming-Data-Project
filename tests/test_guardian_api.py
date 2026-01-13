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

def test_empty_query_raises_value_error(mock_api_key):
    with pytest.raises(ValueError):
        fetch_guardian_articles("")
    
    with pytest.raises(ValueError):
        fetch_guardian_articles(" ")
        
def test_page_size_must_be_positive(mock_api_key):
    with pytest.raises(ValueError):
        fetch_guardian_articles("technology", page_size=0)
    
    with pytest.raises(ValueError):
        fetch_guardian_articles("technology", page_size=-5)

def test_from_date_format(mock_api_key):
    with pytest.raises(ValueError):
        fetch_guardian_articles("technology", from_date="2023/01/01")
    
    with pytest.raises(ValueError):
        fetch_guardian_articles("technology", from_date="01-01-2023")

def test_timeout_bubbles_up(mock_api_key, monkeypatch):
    def timeout_get(*args, **kwargs):
        raise requests.exceptions.Timeout()

    monkeypatch.setattr("src.guardian_api.requests.get", timeout_get)

    with pytest.raises(requests.exceptions.Timeout):
        fetch_guardian_articles("technology")

def test_unexpected_response_shape_raises_runtime_error(mock_api_key, requests_mock):


    requests_mock.get(GUARDIAN_URL, json={'unexpected': {}}, status_code=200)

    with pytest.raises(RuntimeError, match="Unexpected API response format."):
        fetch_guardian_articles("technology")

