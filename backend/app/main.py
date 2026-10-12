from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path
import sqlite3, re

DB_PATH=Path(__file__).resolve().parent.parent / "sample.db"
app=FastAPI(title="AI Code Review Assistant (Mock AI)", version="1.0.0", description="Offline deterministic AI simulation; no API key required.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def db():
    con=sqlite3.connect(DB_PATH); con.row_factory=sqlite3.Row; return con

def init_db():
    with db() as con:
        con.execute("CREATE TABLE IF NOT EXISTS review_history(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT DEFAULT CURRENT_TIMESTAMP,requirement TEXT NOT NULL,findings_count INTEGER NOT NULL)")

@app.on_event("startup")
def startup(): init_db()

@app.get("/api/health")
def health(): return {"status":"ok","mode":"offline-mock-ai"}

class AskIn(BaseModel): question: str = Field(min_length=1,max_length=1000)

class ReviewIn(BaseModel):
    code: str = Field(min_length=1,max_length=12000)
    requirement: str = Field(default="General quality and security",max_length=500)

@app.post("/api/reviews")
def review(item: ReviewIn):
    code=item.code
    findings=[]
    patterns=[("Hard-coded credential-like value",r"(?i)(password|api_key|secret)\s*=\s*['\"][^'\"]{4,}['\"]","high","Use environment variables or a secret manager."),("Dynamic SQL construction",r"(?i)(execute|query)\s*\(.*(\+|f['\"])","high","Use parameterized queries."),("Debug statement",r"(?i)print\s*\(|console\.log\s*\(","low","Remove debug output or use structured logging."),("Broad exception handling",r"except\s*:","medium","Catch specific exception types and handle them explicitly.")]
    for title,pattern,severity,fix in patterns:
        if re.search(pattern,code): findings.append({"title":title,"severity":severity,"recommendation":fix,"requirement":item.requirement})
    if not findings: findings.append({"title":"No seeded risky patterns detected","severity":"info","recommendation":"Add tests and review manually; a clean scan is not proof of correctness.","requirement":item.requirement})
    return {"findings":findings,"finding_count":sum(1 for f in findings if f['severity']!='info'),"summary":"Static pattern scan complete. This mock analyzer does not understand arbitrary program behavior."}

@app.get("/api/checks")
def checks():
    return [{"name":"Health endpoint exists","status":"pass"},{"name":"Input validation configured","status":"pass"},{"name":"Static checks are deterministic","status":"pass"},{"name":"Real semantic AI review","status":"not_implemented"}]

