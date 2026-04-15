# 🚀 Sentiment Analyzer — Feedback Intelligence System

An end-to-end backend-driven application that analyzes customer feedback using an LLM, extracts sentiment and key concerns, and stores results in a PostgreSQL database with real-time visualization.

---

## 📌 Overview

This project is built as part of the Hapticware Backend Hackathon. It provides a complete pipeline from user input to intelligent analysis and data storage.

The system accepts customer feedback, processes it using a Large Language Model (LLM), classifies sentiment (Positive / Neutral / Negative), extracts key concerns, and displays real-time analytics on a frontend dashboard.

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

[ User Input ]
↓
[ Frontend (HTML/JS) ]
↓
POST /feedback API
↓
[ FastAPI Backend ]
↓
[ Groq LLM Processing ]
↓
(JSON Response: sentiment + concern)
↓
[ Store in PostgreSQL ]
↓
[ Return Response to UI ]
↓
[ Update Stats + Feed ]

---

## 🔥 Features

- ✅ Sentiment Classification (Positive / Neutral / Negative)
- ✅ Key Concern Extraction using LLM
- ✅ Handles Mixed Sentiment (e.g., good product but late delivery)
- ✅ Real-time Stats Dashboard
- ✅ Recent Feedback Feed
- ✅ PostgreSQL Integration (DigitalOcean)
- ✅ Clean API Design
- ✅ Error Handling & Validation

---

## 🧠 Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **LLM:** Groq (LLaMA versatile model)
- **Frontend:** HTML, CSS, JavaScript
- **Server:** Uvicorn

---

## 📡 API Endpoints

### 1. Submit Feedback

POST /feedback

#### Request:

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

Returns last 10 feedback entries with sentiment and concerns.

⚙️ Setup Instructions
1. Clone Repository
git clone <your-repo-url>
cd sentiment_analyzer
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Create .env file
GROQ_API_KEY=your_api_key_here
DATABASE_URL=postgresql://doadmin:password@host:port/defaultdb?sslmode=require
5. Run Server
uvicorn main:app --reload
6. Open Application
http://127.0.0.1:8000
🗄️ Database Schema

Table: feedback

Column	Type	Description
id	Integer	Primary Key
customer_id	String	Customer identifier
text	String	Feedback text
sentiment	String	Classified sentiment
concern	String	Extracted key concern
created_at	DateTime	Timestamp (UTC)
🧠 Key Implementation Details
Used prompt engineering to ensure accurate sentiment detection
Handled mixed sentiment cases intelligently
Stored timestamps in UTC and converted to local time in frontend
Implemented fallback handling for inconsistent LLM outputs
Designed modular backend structure
🎯 Hackathon Requirements Covered
✅ Backend Service (FastAPI)
✅ API Endpoints
✅ PostgreSQL Integration
✅ LLM Integration
✅ Basic Frontend
✅ End-to-End Working System
🚀 Future Improvements
Add authentication system
Deploy application (Render / AWS)
Add advanced analytics dashboard
Improve UI/UX
Add sentiment trend graphs
👨‍💻 Team

Breed Varpe, Dheerendra Pratap Singh Solanki
Team: Byte Me

📌 Conclusion

This project demonstrates a complete backend architecture integrating APIs, database, and LLM capabilities to build a real-world feedback intelligence system. It is designed to be scalable, efficient, and production-ready.
```
