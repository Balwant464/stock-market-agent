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

# ✅ Fetch API Keys from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")  # 🔹 Stock news API

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Fetch Stock Market Price using `yfinance`
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="5d")  # 🔹 Fetch last 5 days to analyze trend

        if data.empty:
            return None, "Stock price not available"

        latest_price = round(data["Close"].iloc[-1], 2)
        prev_price = round(data["Close"].iloc[-2], 2)

        return latest_price, prev_price
    except Exception as e:
        return None, f"Error fetching stock price: {str(e)}"

# ✅ Fetch Stock News using Alpha Vantage API
def get_stock_news(ticker):
    if not ALPHA_VANTAGE_API_KEY:
        return "Stock news API key missing."

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url)
        news_data = response.json()

        if "feed" in news_data:
            top_news = news_data["feed"][:3]  # Get top 3 news articles
            news_summary = "\n".join([f"🔹 {item['title']} - {item['url']}" for item in top_news])
            return news_summary
        return "No recent stock news available."
    except Exception as e:
        return f"Error fetching stock news: {str(e)}"

# ✅ AI Agent for Stock Analysis
class StockMarketAgent:
    def __init__(self):
        try:
            if not GOOGLE_API_KEY:
                raise ValueError("Missing GOOGLE_GEMINI_API_KEY in .env file")
            
            self.llm = GoogleGenerativeAI(
                model="gemini-1.5-pro",
                google_api_key=GOOGLE_API_KEY
            )
        except Exception as e:
            print(f"Error initializing AI model: {str(e)}")
            self.llm = None

    def get_stock_analysis(self, ticker):
        latest_price, prev_price = get_stock_price(ticker)
        if latest_price is None:
            return {"ticker": ticker, "price": prev_price, "analysis": "Stock price not available."}

        # 🔹 Determine Buy/Sell/Hold Recommendation
        if latest_price > prev_price:
            recommendation = "📈 Buy - The stock is trending upwards."
        elif latest_price < prev_price:
            recommendation = "📉 Sell - The stock is declining."
        else:
            recommendation = "⚖️ Hold - The stock is stable."

        stock_news = get_stock_news(ticker)

        prompt = (
            f"Analyze the stock {ticker} with the current price ${latest_price}. "
            "Provide 5 key insights about stock market trends, company financials, competition, valuation, and risk factors. "
            "Additionally, suggest a Buy/Sell/Hold decision based on the stock's recent price trend and market sentiment."
        )

        try:
            analysis = self.llm.invoke(prompt) if self.llm else "AI model not available."
            if not analysis:
                analysis = "AI response was empty. Try again later."
        except Exception as e:
            analysis = f"Error generating analysis: {str(e)}"

        return {
            "ticker": ticker,
            "price": f"${latest_price}",
            "recommendation": recommendation,
            "analysis": analysis,
            "latest_news": stock_news
        }

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
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
