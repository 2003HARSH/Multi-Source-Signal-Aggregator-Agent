from typing import TypedDict, List

class AgentState(TypedDict):
    """
    Represents the shared state of the multi-agent system.
    """
    tickers: List[str]
    data: dict
    news: dict
    sentiment: dict
    decision: List[dict]
