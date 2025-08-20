from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import Literal
from app.state import AgentState

# 1. Define the desired structured output, now including a 'reason'
class StockSignal(BaseModel):
    """The signal, confidence, and reasoning for a stock."""
    signal: Literal["Buy", "Hold", "Sell"] = Field(description="The investment signal for the stock.")
    confidence: int = Field(description="The confidence in the signal, from 0 to 100.")
    reason: str = Field(description="A brief, natural language reason for the signal.")

    @validator('confidence')
    def confidence_must_be_in_range(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Confidence must be between 0 and 100')
        return v

def decision_agent(state: AgentState) -> dict:
    """
    Generates a structured Buy/Hold/Sell signal, confidence, and reason for each stock.
    """
    print("---MAKING DECISION---")
    
    # 2. Bind the Pydantic model to the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    structured_llm = llm.with_structured_output(StockSignal)
    
    final_decisions = []

    for ticker in state['tickers']:
        # Updated prompt to explicitly ask for a reason
        prompt = f"""
        Given the following data for stock ticker {ticker}, provide a Buy, Hold, or Sell signal, a confidence score, and a brief reason for your decision.

        - **Latest Price:** {state['data'].get(ticker, {}).get('price', 'N/A')}
        - **Trading Volume:** {state['data'].get(ticker, {}).get('volume', 'N/A')}
        - **Sentiment Summary:** {state['sentiment'].get(ticker, 'N/A')}
        - **Key Headlines:** {', '.join(state['news'].get(ticker, []))}
        """
        
        try:
            # 3. Invoke the structured LLM
            response = structured_llm.invoke(prompt)
            signal = response.signal
            confidence = f"{response.confidence}%"
            reason = response.reason

        except Exception as e:
            print(f"Error making decision for {ticker}: {e}")
            signal = "Error"
            confidence = "N/A"
            reason = "An error occurred during analysis."

        # 4. Append the full structured result
        final_decisions.append({
            "ticker": ticker,
            "price": state['data'].get(ticker, {}).get('price', 'N/A'),
            "signal": signal,
            "confidence": confidence,
            "reason": reason, # Include the reason in the final output
            "sentiment": state['sentiment'].get(ticker, "N/A"),
            "headlines": state['news'].get(ticker, [])
        })

    return {"decision": final_decisions}
