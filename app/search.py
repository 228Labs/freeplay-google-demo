from typing import Any

from tavily import TavilyClient

client = TavilyClient()


def tavily_search(query: str) -> dict[str, Any]:
    """
    Search the web using tavily. The query should be a high quality natural
    language query, suitable for input to Google Search or any other information
    retrieval system. The results will be a list of raw search results, that are
    relevant to the query.
    """
    return client.search(
        query, max_results=3, search_depth="basic", include_raw_content=True
    )
