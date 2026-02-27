# web_search.py
import serpapi
import os

#------------------------------------------------------------------------
# Tool Function
#-----------------------------------------------------------------------
def web_search(query: str, recency_days=None, domains=None):
    client = serpapi.Client(api_key=os.getenv("SERPAPI_KEY"))

    params = {
        "engine": "google",
        "q": query, 
        "num" : 10
    }

    

    # Optional: domain filtering (Google uses site: syntax)
    # If a domain is mentioned (eg. Wikipedia.org or Ign.com)
    # Combine it with the query
    if domains:
        domain_filters = " OR ".join([f"site:{d}" for d in domains])
        params["q"] = f"{query} ({domain_filters})"

   
    # Optional: recency filter 
    # Google uses tbs=qdr:X where X = number + unit
    # d = days, w = weeks, m = months, y = years
    #
    # Example: recency_days=7 → qdr:7d
    if recency_days:
        params["tbs"] = f"qdr:{recency_days}d"

    results = client.search(params)

    return {
        "query": query,
        "domains": domains,
        "recency_days": recency_days,
        "results": results.get("organic_results", [])
    }
