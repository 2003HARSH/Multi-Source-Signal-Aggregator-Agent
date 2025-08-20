from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.agents.data_agent import data_agent
from app.agents.news_agent import news_agent
from app.agents.sentiment_agent import sentiment_agent
from app.agents.decision_agent import decision_agent

def build_workflow():
    """
    Builds the multi-agent workflow using LangGraph.
    """
    workflow = StateGraph(AgentState)

    # Add nodes for each agent
    workflow.add_node("data_agent", data_agent)
    workflow.add_node("news_agent", news_agent)
    workflow.add_node("sentiment_agent", sentiment_agent)
    workflow.add_node("decision_agent", decision_agent)

    # Define the sequence of execution
    workflow.set_entry_point("data_agent")
    workflow.add_edge("data_agent", "news_agent")
    workflow.add_edge("news_agent", "sentiment_agent")
    workflow.add_edge("sentiment_agent", "decision_agent")
    workflow.add_edge("decision_agent", END)

    # Compile the graph into a runnable app
    # The checkpointer allows for persisting state, which is good practice
    # For this simple app, we'll use an in-memory checkpointer.
    return workflow.compile()
