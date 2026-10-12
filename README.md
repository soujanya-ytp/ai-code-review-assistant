# AI Code Review Assistant (Mock AI)

Inspect submitted code snippets for seeded quality and security issues, map findings to requirements, and run a tiny local test suite.

## What this is

This is a self-contained full-stack sample for testing an FDE repository/application evaluator. The mock AI is a deterministic static-analysis demo, not a general-purpose code understanding model. It uses safe pattern checks and local test cases.

## Stack
- React + Vite frontend
- Python FastAPI backend
- SQLite local database (seeded on startup)
- Docker Compose
- pytest smoke tests

## Run with Docker

```bash
docker compose up --build
```

Open http://localhost:5173. API docs: http://localhost:8000/docs. Health check: http://localhost:8000/api/health. No API keys or external AI services are required.

## Run locally without Docker

Backend (Python 3.11+):
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (Node 20+): in another terminal run `cd frontend && npm install && npm run dev`.

## Test backend

```bash
cd backend
pytest -q
```

## Evaluation scenarios
- Submit code snippets for analysis
- Detect common risky patterns
- Map findings to requirement labels
- Run included deterministic checks
- Invalid inputs should return validation errors.
- Empty/no-match results should be handled without crashing.
- Refreshing the browser should retain persisted records (SQLite).
- API errors should not silently appear as successful results.
- Inspect whether the UI clearly labels mock AI output and its limitations.

## Limitations
This is a sample benchmark, not a production-ready system. The AI behavior is deterministic and limited; there is no real model inference, external integration, or claim of semantic understanding. Add stronger auth, migrations, observability, and broader tests for production use.
