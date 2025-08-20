from langchain_google_genai import ChatGoogleGenerativeAI
from app.state import AgentState

def sentiment_agent(state: AgentState) -> dict:
    """
    Analyzes the sentiment of news headlines for each stock.
    """
    print("---ANALYZING SENTIMENT---")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    sentiment_results = {}

    for ticker, headlines in state['news'].items():
        if not headlines:
            sentiment_results[ticker] = "No headlines found to analyze."
            continue
        
        prompt = f"""Analyze the overall sentiment of these news headlines for {ticker} and provide a brief, neutral summary of the sentiment (e.g., "Positive due to strong earnings report", "Negative on market fears", "Mixed following product announcement").

        Headlines:
        - {"\\n- ".join(headlines)}

        Sentiment Summary:"""
        
        try:
            response = llm.invoke(prompt)
            sentiment_results[ticker] = response.content.strip()
        except Exception as e:
            print(f"Error analyzing sentiment for {ticker}: {e}")
            sentiment_results[ticker] = "Error during analysis."

    return {"sentiment": sentiment_results}
