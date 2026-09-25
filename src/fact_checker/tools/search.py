from tavily import TavilyClient


def search_web(query: str, max_results: int = 5, api_key: str | None = None) -> list[dict]:
    """Search the web and return a list of {url, title, content} dicts."""
    client = TavilyClient(api_key=api_key)
    response = client.search(query=query, max_results=max_results)
    return [
        {
            "url": r.get("url", ""),
            "title": r.get("title", ""),
            "content": r.get("content", ""),
        }
        for r in response.get("results", [])
    ]
