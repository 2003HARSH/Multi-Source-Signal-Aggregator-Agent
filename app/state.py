from typing import TypedDict, List, Dict

# State for the sub-graph that processes a single ticker
class TickerAnalysisState(TypedDict):
    ticker: str
    data: Dict
    news: List[str]
    sentiment: str
    decision: Dict

# State for the main workflow that manages the parallel execution
class AgentState(TypedDict):
    tickers: List[str]
    results: List[Dict] # This will hold the final aggregated results
