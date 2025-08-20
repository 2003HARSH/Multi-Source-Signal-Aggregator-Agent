import yfinance as yf
from app.state import TickerAnalysisState

def data_agent(state: TickerAnalysisState) -> dict:
    """
    Fetches the latest price and volume for a single stock ticker.
    """
    print(f"---FETCHING DATA FOR {state['ticker']}---")
    ticker = state['ticker']
    data_results = {}
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            data_results = {
                "price": f"{hist['Close'].iloc[-1]:.2f}",
                "volume": f"{hist['Volume'].iloc[-1]:,}"
            }
        else:
             data_results = {"price": "N/A", "volume": "N/A"}
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        data_results = {"price": "Error", "volume": "Error"}
            
    return {"data": data_results}
