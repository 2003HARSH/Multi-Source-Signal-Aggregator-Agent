import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from app.workflow import build_workflow

load_dotenv()
app = FastAPI(
    title="Multi-Source Signal Aggregator API",
    description="An API that uses a multi-agent system to generate stock signals.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TickerRequest(BaseModel):
    tickers: List[str]

app_graph = build_workflow()

@app.post("/signals")
async def get_signals(request: TickerRequest):
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        return {"error": "API keys for Google or Tavily are not set."}

    inputs = {"tickers": request.tickers}
    final_state = app_graph.invoke(inputs)
    
    # Use the 'results' key from the new AgentState
    return {"results": final_state.get('results', [])}

@app.get("/")
def read_root():
    return {"status": "API is running"}
