from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import Literal
from app.state import TickerAnalysisState

class StockSignal(BaseModel):
    signal: Literal["Buy", "Hold", "Sell"] = Field(description="The investment signal.")
    confidence: int = Field(description="Confidence in the signal (0-100).")
    reason: str = Field(description="A brief reason for the signal.")

def decision_agent(state: TickerAnalysisState) -> dict:
    """
    Generates a structured signal for a single stock.
    """
    ticker = state['ticker']
    print(f"---MAKING DECISION FOR {ticker}---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    structured_llm = llm.with_structured_output(StockSignal)
    
    prompt = f"""
    Given the data for {ticker}, provide a Buy/Hold/Sell signal, confidence score, and reason.
    - Price: {state['data'].get('price', 'N/A')}
    - Volume: {state['data'].get('volume', 'N/A')}
    - Sentiment: {state.get('sentiment', 'N/A')}
    - Headlines: {', '.join(state.get('news', []))}
    """
    
    try:
        response = structured_llm.invoke(prompt)
        decision = {
            "ticker": ticker,
            "price": state['data'].get('price', 'N/A'),
            "signal": response.signal,
            "confidence": f"{response.confidence}%",
            "reason": response.reason,
            "sentiment": state.get('sentiment', "N/A"),
            "headlines": state.get('news', [])
        }
    except Exception as e:
        print(f"Error making decision for {ticker}: {e}")
        decision = {"ticker": ticker, "signal": "Error", "reason": str(e)}

    return {"decision": decision}
