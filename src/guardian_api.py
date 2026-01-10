import os
from urllib import response
import requests

GUARDIAN_API_URL = "https://content.guardianapis.com/search"

def fetch_guardian_articles(query, from_date=None, page_size=10):
    API_KEY = os.getenv("GUARDIAN_API_KEY")
    
    if not API_KEY:
        raise RuntimeError("Guardian API key not set in environment variables.")
    
    params = {
        "q": query,
        "page-size": page_size,
        "api-key": API_KEY,
        "show-fields": "headline, trailText"
    }
    
    if from_date:
        params["from-date"] = from_date
    
    response = requests.get(GUARDIAN_API_URL, params=params)
    response.raise_for_status()
    
    data = response.json()
    return data["response"]["results"]

# if __name__ == "__main__":
#     articles = fetch_guardian_articles("Technology", from_date="2023-01-01", page_size=6)
#     print(f"Fetched {len(articles)} articles:")