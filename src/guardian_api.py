import os
from urllib import response
import requests

GUARDIAN_API_URL = "https://content.guardianapis.com/search"

def fetch_guardian_articles(query, from_date=None, page_size=10):
    API_KEY = os.getenv("GUARDIAN_API_KEY")
    
    if not API_KEY:
        raise RuntimeError("Guardian API key not set in environment variables.")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string.")
    
    if not isinstance(page_size, int) or page_size <= 0:
        raise ValueError("Page size must be a positive integer.")
    
    if from_date is not None:
        try:
            from datetime import datetime
            datetime.strptime(from_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("from_date must be in 'YYYY-MM-DD' format.")
    
    params = {
        "q": query,
        "page-size": page_size,
        "api-key": API_KEY,
        "show-fields": "headline, trailText"
    }
    
    if from_date:
        params["from-date"] = from_date
    
    response = requests.get(GUARDIAN_API_URL, params=params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    try:
        results = data["response"]["results"]
    except (TypeError, KeyError):
        raise RuntimeError("Unexpected API response format.")
    return list(results)

# if __name__ == "__main__":
#     articles = fetch_guardian_articles("Technology", from_date="2023-01-01", page_size=6)
#     print(f"Fetched {len(articles)} articles:")