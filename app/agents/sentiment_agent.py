from langchain_google_genai import ChatGoogleGenerativeAI
from app.state import TickerAnalysisState

def sentiment_agent(state: TickerAnalysisState) -> dict:
    """
    Analyzes sentiment for a single stock's news headlines.
    """
    ticker = state['ticker']
    headlines = state['news']
    print(f"---ANALYZING SENTIMENT FOR {ticker}---")

    if not headlines:
        return {"sentiment": "No headlines found to analyze."}
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    prompt = f"""Analyze the overall sentiment of these news headlines for {ticker} and provide a brief, neutral summary.

    Headlines:
    - {"\\n- ".join(headlines)}

    Sentiment Summary:"""
    
    try:
        response = llm.invoke(prompt)
        sentiment = response.content.strip()
    except Exception as e:
        print(f"Error analyzing sentiment for {ticker}: {e}")
        sentiment = "Error during analysis."

    return {"sentiment": sentiment}
