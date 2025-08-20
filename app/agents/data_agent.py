import yfinance as yf
from app.state import AgentState

def data_agent(state: AgentState) -> dict:
    """
    Fetches the latest price and volume for each stock ticker.
    """
    print("---FETCHING STOCK DATA---")
    data_results = {}
    for ticker in state['tickers']:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                data_results[ticker] = {
                    "price": f"{hist['Close'].iloc[-1]:.2f}",
                    "volume": f"{hist['Volume'].iloc[-1]:,}"
                }
            else:
                 data_results[ticker] = {"price": "N/A", "volume": "N/A"}
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            data_results[ticker] = {"price": "Error", "volume": "Error"}
            
    return {"data": data_results}
