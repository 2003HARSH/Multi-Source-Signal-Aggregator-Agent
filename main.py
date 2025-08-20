import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from app.workflow import build_workflow

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(
    title="Multi-Source Signal Aggregator API",
    description="An API that uses a multi-agent system to generate stock signals.",
    version="1.0.0"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the request model using Pydantic
class TickerRequest(BaseModel):
    tickers: List[str]

# Build the LangGraph workflow once when the app starts
app_graph = build_workflow()

@app.post("/signals")
async def get_signals(request: TickerRequest):
    """
    Accepts a list of stock tickers and returns a buy/hold/sell signal for each.
    """
    # Check for necessary API keys
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        return {"error": "API keys for Google or Tavily are not set."}

    inputs = {"tickers": request.tickers}
    
    # Run the LangGraph workflow
    final_state = app_graph.invoke(inputs)
    
    return {"results": final_state.get('decision', [])}

@app.get("/")
def read_root():
    """
    Root endpoint for health check.
    """
    return {"status": "API is running"}

# To run this server:
# 1. Make sure you have installed dependencies with `uv pip install -e .`
# 2. Run the command: uvicorn main:app --reload
