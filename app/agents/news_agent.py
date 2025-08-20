from langchain_community.tools.tavily_search import TavilySearchResults
from app.state import TickerAnalysisState

def news_agent(state: TickerAnalysisState) -> dict:
    """
    Fetches news headlines for a single stock ticker.
    """
    ticker = state['ticker']
    print(f"---FETCHING NEWS FOR {ticker}---")
    
    tavily_tool = TavilySearchResults(max_results=5)
    headlines = []
    try:
        search_results = tavily_tool.invoke({"query": f"latest financial news on {ticker}"})
        headlines = [res["title"] for res in search_results]
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")

    return {"news": headlines}
