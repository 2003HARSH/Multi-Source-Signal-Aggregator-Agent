from langgraph.graph import StateGraph, END
from app.state import AgentState, TickerAnalysisState
from app.agents.data_agent import data_agent
from app.agents.news_agent import news_agent
from app.agents.sentiment_agent import sentiment_agent
from app.agents.decision_agent import decision_agent

def build_single_ticker_graph():
    """
    Builds the sequential workflow for analyzing a single stock.
    This is our sub-graph.
    """
    workflow = StateGraph(TickerAnalysisState)

    workflow.add_node("data_agent", data_agent)
    workflow.add_node("news_agent", news_agent)
    workflow.add_node("sentiment_agent", sentiment_agent)
    workflow.add_node("decision_agent", decision_agent)

    workflow.set_entry_point("data_agent")
    workflow.add_edge("data_agent", "news_agent")
    workflow.add_edge("news_agent", "sentiment_agent")
    workflow.add_edge("sentiment_agent", "decision_agent")
    workflow.add_edge("decision_agent", END)

    return workflow.compile()

def build_workflow():
    """
    Builds the main workflow that runs the single-ticker analysis in parallel.
    """
    # Compile the sub-graph that will be run in parallel
    single_ticker_graph = build_single_ticker_graph()

    def run_parallel_analysis(state: AgentState):
        """
        This node runs the single_ticker_graph for each ticker concurrently.
        """
        # Prepare the initial state for each parallel run
        ticker_states = [{"ticker": t} for t in state['tickers']]
        
        # Use .batch() to execute the sub-graph on all inputs in parallel
        # max_concurrency can be adjusted based on your system's capabilities
        results = single_ticker_graph.batch(ticker_states, {"max_concurrency": 5})
        
        # Extract the final decision from each parallel run's state
        final_decisions = [run_result['decision'] for run_result in results]
        
        return {"results": final_decisions}

    # Define the main workflow
    workflow = StateGraph(AgentState)
    workflow.add_node("parallel_analysis", run_parallel_analysis)
    workflow.set_entry_point("parallel_analysis")
    workflow.add_edge("parallel_analysis", END)

    return workflow.compile()
