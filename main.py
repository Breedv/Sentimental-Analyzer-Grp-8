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


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    email = Column(String)
    category = Column(String)
    urgency = Column(String)
    sentiment = Column(String)
    concern = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create table if not exists
Base.metadata.create_all(bind=engine)

class TicketRequest(BaseModel):
    email: str
    ticket_text: str

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
# TICKET CLASSIFIER AGENT
# =========================
@app.post("/agent/ticket-classifier")
async def classify_ticket(req: TicketRequest):

    # ✅ Validation
    if not req.email or not req.ticket_text:
        raise HTTPException(status_code=400, detail="Invalid input")

    try:
        print("Incoming request:", req.ticket_text)

        prompt = f"""
You are a support ticket classification agent.

Return ONLY valid JSON:

{{
  "sentiment": "Positive / Neutral / Negative",
  "category": "Billing / Technical / General",
  "urgency": "High / Medium / Low",
  "concern": "one short summary"
}}

Ticket:
{req.ticket_text}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        raw = response.choices[0].message.content.strip()
        print("LLM RAW:", raw)

        # Clean markdown
        raw = raw.replace("```json", "").replace("```", "").strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise Exception("No valid JSON found")

        result = json.loads(match.group())

        # SAFETY FALLBACK (VERY IMPORTANT)
        result.setdefault("sentiment", "Neutral")
        result.setdefault("category", "General")
        result.setdefault("urgency", "Medium")
        result.setdefault("concern", "No concern")

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


    db = SessionLocal()

    record = Ticket(
        text=req.ticket_text,
        email=req.email,
        category=result["category"],
        urgency=result["urgency"],
        sentiment=result["sentiment"],
        concern=result["concern"]
    )

    db.add(record)
    db.commit()
    db.close()


    return {
        "email": req.email,
        "sentiment": result["sentiment"],
        "category": result["category"],
        "urgency": result["urgency"],
        "concern": result["concern"]
    }

@app.get("/feedback/stats")
async def sentiment_stats():
    db = SessionLocal()

    results = db.query(
        Ticket.sentiment,
        func.count()
    ).group_by(Ticket.sentiment).all()

    total = sum(row[1] for row in results)
    stats = {row[0]: row[1] for row in results}

    db.close()

    return {
        "stats": stats,
        "total": total
    }

@app.get("/feedback/recent")
async def recent_feedback():
    db = SessionLocal()

    records = db.query(Ticket)\
        .order_by(Ticket.created_at.desc())\
        .limit(10).all()

    result = [
        {
            "email": r.email,
            "text": r.text,
            "sentiment": r.sentiment,
            "category": r.category,
            "urgency": r.urgency,
            "concern": r.concern,
            "created_at": r.created_at.isoformat() if r.created_at else ""
        }
        for r in records
    ]

    db.close()
    return result