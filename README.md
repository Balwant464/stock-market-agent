# 📈 Stock Market Agent

Welcome to the **Stock Market Agent**, an AI-powered API that provides stock market insights. This project integrates **FastAPI**, **LangChain**, **Google Gemini AI**, and **Yahoo Finance** to fetch stock prices and generate insightful analysis in plain text format.

## 🚀 Features

- **Fetch Real-Time Stock Prices**: Uses `yfinance` to retrieve the latest stock price.
- **AI-Powered Analysis**: Leverages `Google Gemini AI` to generate an in-depth stock market analysis.
- **FastAPI Framework**: A lightweight and high-performance API for quick responses.
- **Secure API Key Management**: Uses `.env` files to securely store API keys.
- **Public API Access**: Deployable on a public server for easy access via Postman, curl, or a browser.

## 📦 Technologies Used

- **FastAPI** - For building the API service.
- **Google Gemini AI** - For generating stock analysis insights.
- **Yahoo Finance (`yfinance`)** - For fetching real-time stock prices.
- **Uvicorn** - For running the FastAPI server.
- **dotenv (`python-dotenv`)** - For secure environment variable handling.
- **LangChain (`langchain_google_genai`)** - For AI integration.
- **Git & GitHub** - For version control and repository management.

---

## 🛠️ Setup & Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/Balwant464/stock-market-agent.git
cd stock-market-agent
```

### **2️⃣ Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Configure API Keys**
Create a `.env` file and add your **Google Gemini API Key**:
```sh
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

---

## 🎯 How to Run the API

### **Start the Server**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **Test the API**
Open a browser or use `curl` to test:
```sh
curl http://127.0.0.1:8000/
```
or visit in your browser: `http://127.0.0.1:8000/`

### **Fetch Stock Analysis**
```sh
curl http://127.0.0.1:8000/stock/TSLA
```
Example Response:
```json
{
    "ticker": "TSLA",
    "price": "$267.28",
    "analysis": "Tesla's stock remains highly volatile, influenced by ... (detailed analysis)"
}
```

---

## 🌍 Deploying on a Public Server

You can deploy this API on a cloud platform like:
- **Render** (Free deployment available)
- **Railway** (Easy to set up)
- **Google Cloud Run** (Scalable deployment)
- **AWS EC2** (For more control)

### **Deploy on Render (Example)**
1. Create a new service on [Render](https://render.com/).
2. Connect your GitHub repository.
3. Set environment variables (`GOOGLE_GEMINI_API_KEY`).
4. Deploy and get a public API URL.

---

## 🛡️ License
This project is **MIT Licensed**. Feel free to use and modify it as needed.

---

🔥 **Happy Coding!** 🔥

