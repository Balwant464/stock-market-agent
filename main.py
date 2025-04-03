import os
import requests
import nest_asyncio
from fastapi import FastAPI
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import uvicorn
import yfinance as yf

# ✅ Load environment variables
load_dotenv()

# ✅ Fetch API Key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Fetch Stock Market Price using `yfinance`
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if data.empty:
            return "Stock price not available"
        return f"${data['Close'].iloc[-1]:.2f}"
    except Exception as e:
        return f"Error fetching stock price: {str(e)}"

# ✅ AI Agent for Stock Analysis
class StockMarketAgent:
    def __init__(self):
        try:
            if not GOOGLE_API_KEY:
                raise ValueError("Missing GOOGLE_GEMINI_API_KEY in .env file")
            
            self.llm = GoogleGenerativeAI(
                model="gemini-1.5-pro",  # 🔹 Updated Model Name
                google_api_key=GOOGLE_API_KEY
            )
        except Exception as e:
            print(f"Error initializing AI model: {str(e)}")
            self.llm = None

    def get_stock_analysis(self, ticker):
        price = get_stock_price(ticker)
        if self.llm is None:
            return {"ticker": ticker, "price": price, "analysis": "AI model not initialized"}

        prompt = (
            f"Analyze the stock {ticker} with the current price {price}. "
            "Provide exactly 5 key insights about the stock market trends, company financials, competition, valuation, and risk factors. "
            "Ensure the response is in plain text and structured in a readable format. "
            "Do not return JSON format, only human-readable text."
        )

        try:
            analysis = self.llm.invoke(prompt)
            if not analysis:
                return {"ticker": ticker, "price": price, "analysis": "Empty response from AI"}
        except Exception as e:
            analysis = f"Error generating analysis: {str(e)}"

        return {"ticker": ticker, "price": price, "analysis": analysis}

agent = StockMarketAgent()

# ✅ Root Endpoint (Check if API is running)
@app.get("/")
def read_root():
    return {"message": "Stock Market Agent API is running! Use /stock/{ticker} to get analysis."}

# ✅ API Endpoint to Get Stock Analysis
@app.get("/stock/{ticker}")
async def get_stock_info(ticker: str):
    response = agent.get_stock_analysis(ticker)
    return response

# ✅ Run API Server with `uvicorn`
if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)  # 🔹 Runs continuously