# 🚀 Sentiment Analyzer — Feedback Intelligence System

An end-to-end backend-driven application that analyzes customer feedback using an LLM, extracts sentiment and key concerns, and stores results in a PostgreSQL database with real-time visualization.

---

## 📌 Overview

This project processes customer feedback using a Large Language Model (LLM), classifies sentiment (Positive / Neutral / Negative), extracts key concerns, and displays analytics on a dashboard.

---

## 🏗️ Architecture

User (Frontend UI)
↓
FastAPI Backend (API Layer)
↓
Groq LLM (Sentiment + Concern Extraction)
↓
PostgreSQL Database (Storage)
↓
Frontend Dashboard (Stats + Recent Feedback)

---

## 🔄 Flowchart

User Input
↓
Frontend (HTML/JS)
↓
POST /feedback API
↓
FastAPI Backend
↓
Groq LLM Processing
↓
(JSON Response: sentiment + concern)
↓
Store in PostgreSQL
↓
Return Response to UI
↓
Update Stats + Feed

---

## 🔥 Features

- Sentiment classification (Positive / Neutral / Negative)
- Key concern extraction
- Handles mixed sentiment
- Real-time dashboard
- PostgreSQL integration

---

## 🧠 Tech Stack

- FastAPI
- PostgreSQL (SQLAlchemy)
- Groq LLM
- HTML, CSS, JavaScript
- Uvicorn

---

## 📡 API Endpoints

### 1. Submit Feedback

POST /feedback

Request:

```json
{
  "customer_id": "cust_001",
  "text": "Delivery was late but product is great"
}

Response:

{
  "sentiment": "Neutral",
  "key_concern": "late delivery but product quality is good"
}

2. Get Sentiment Stats
GET /feedback/stats

Response:

{
  "stats": {
    "Positive": 5,
    "Neutral": 3,
    "Negative": 2
  },
  "total": 10
}

3. Get Recent Feedback
GET /feedback/recent

Returns last 10 feedback entries.

⚙️ Setup Instructions
Clone Repo
git clone <your-repo-url>
cd sentiment_analyzer
Create Virtual Environment
python -m venv venv
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Create .env
GROQ_API_KEY=your_api_key_here
DATABASE_URL=postgresql://doadmin:password@host:port/defaultdb?sslmode=require
Run Server
uvicorn main:app --reload

🗄️ Database Schema
Column	Type	Description
id	Integer	Primary Key
customer_id	String	Customer ID
text	String	Feedback
sentiment	String	Sentiment
concern	String	Key Concern
created_at	DateTime	Timestamp

🎯 Hackathon Requirements Covered
Backend (FastAPI)
API Endpoints
PostgreSQL Integration
LLM Integration
Frontend UI
👨‍💻 Team

Breed Varpe
Team Byte Me

📌 Conclusion

This project demonstrates a complete backend system integrating APIs, database, and LLM for intelligent feedback analysis.
```
