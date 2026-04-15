from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import json, os, re

# Load env
load_dotenv()

# =========================
# DATABASE SETUP
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =========================
# GROQ CLIENT
# =========================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# MODEL
# =========================
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String)
    text = Column(String)
    sentiment = Column(String)
    concern = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create table
Base.metadata.create_all(bind=engine)

# =========================
# REQUEST SCHEMA
# =========================
class FeedbackRequest(BaseModel):
    text: str
    customer_id: str

# =========================
# FASTAPI APP
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

# =========================
# SENTIMENT API
# =========================
@app.post("/feedback")
async def analyze_sentiment(req: FeedbackRequest):
    try:
        print("Incoming request:", req.text)

        prompt = f"""
You are an AI that analyzes customer feedback.

Return ONLY valid JSON (no explanation):
{{
  "sentiment": "Positive" or "Neutral" or "Negative",
  "key_concern": "short one-line issue"
}}

Feedback: {req.text}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        raw = response.choices[0].message.content.strip()
        print("LLM RAW:", raw)

        # Clean response
        raw = raw.replace("```json", "").replace("```", "").strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise Exception("No valid JSON found in LLM response")

        result = json.loads(match.group())

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    # Save to DB
    db = SessionLocal()
    record = Feedback(
        customer_id=req.customer_id,
        text=req.text,
        sentiment=result.get("sentiment"),
        concern=result.get("key_concern")
    )
    db.add(record)
    db.commit()
    db.close()

    return result

# =========================
# STATS API
# =========================
@app.get("/feedback/stats")
async def sentiment_stats():
    db = SessionLocal()

    results = db.query(
        Feedback.sentiment,
        func.count()
    ).group_by(Feedback.sentiment).all()

    total = sum(row[1] for row in results)
    stats = {row[0]: row[1] for row in results}

    db.close()

    return {
        "stats": stats,
        "total": total
    }

# =========================
# RECENT FEEDBACK API
# =========================
@app.get("/feedback/recent")
async def recent_feedback():
    db = SessionLocal()

    records = db.query(Feedback)\
        .order_by(Feedback.created_at.desc())\
        .limit(10).all()

    result = [
        {
            "customer_id": r.customer_id,
            "text": r.text,
            "sentiment": r.sentiment,
            "concern": r.concern,
            "created_at": r.created_at.isoformat() if r.created_at else ""
        }
        for r in records
    ]

    db.close()
    return result