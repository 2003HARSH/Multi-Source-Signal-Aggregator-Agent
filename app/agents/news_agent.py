from langchain_community.tools.tavily_search import TavilySearchResults
from app.state import AgentState



def news_agent(state: AgentState) -> dict:
    """
    Fetches the top 5 recent news headlines for each stock ticker.
    """
    print("---FETCHING NEWS---")
    # Initialize the tool once to be used by the agent
    tavily_tool = TavilySearchResults(max_results=5)
    news_results = {}
    for ticker in state['tickers']:
        try:
            search_results = tavily_tool.invoke({"query": f"latest financial news on {ticker}"})
            headlines = [res["title"] for res in search_results]
            news_results[ticker] = headlines
        except Exception as e:
            print(f"Error fetching news for {ticker}: {e}")
            news_results[ticker] = []

    return {"news": news_results}