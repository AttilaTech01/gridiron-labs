# Gridiron Labs

A fantasy football companion app for **Power Users** and **Busy Managers**. Gridiron Labs translates complex NFL data into simple, actionable start/sit recommendations — a confidence grade in five seconds, five minutes of data if you want it.

Users build their own roster directly in the app, set their weekly lineup, and let the engine do the rest.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Frontend | Vite + React + TypeScript + Tailwind CSS + shadcn/ui |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Cache | Redis |
| Auth | Clerk |
| DB Migrations | Alembic |

---

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker Desktop

---

## Project Structure

```
gridiron-labs/
├── frontend/         # Vite + React + TypeScript
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── hooks/
│       ├── store/
│       ├── lib/
│       └── types/
├── backend/          # FastAPI + Python
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/     # config, database, auth, cache
│   │   ├── models.py
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── db/           # Alembic migrations
│   ├── tests/
│   └── requirements.txt
└── docker-compose.yml
```

---

## Getting Started

### 1. Start the database and cache

From the root `gridiron-labs/` folder:

```bash
docker-compose up -d
```

This starts PostgreSQL on port `5432` and Redis on port `6379`.

### 2. Start the backend

```bash
cd backend
.\.venv\Scripts\Activate.ps1        # Windows
# source .venv/bin/activate         # Mac/Linux

pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`  
Auto-generated API docs: `http://localhost:8000/docs`

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## Environment Variables

### Backend (`backend/.env`)

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gridiron
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
CLERK_SECRET_KEY=
```

### Frontend (`frontend/.env.local`)

```
VITE_API_URL=http://localhost:8000
VITE_CLERK_PUBLISHABLE_KEY=
```

---

## Database & Migrations (Alembic)

All commands are run from the `backend/` folder with the virtual environment active.

### Apply all pending migrations
```bash
python -m alembic upgrade head
```

### Generate a new migration after changing models
```bash
python -m alembic revision --autogenerate -m "describe your change"
```
Always run `upgrade head` after generating a migration to apply it.

### Roll back one migration
```bash
python -m alembic downgrade -1
```

### Roll back everything (reset to empty database)
```bash
python -m alembic downgrade base
```

### Check current migration status
```bash
python -m alembic current
```

### View migration history
```bash
python -m alembic history
```

---

## Workflow: Adding or Changing a Model

1. Edit `app/models.py`
2. Generate the migration: `python -m alembic revision --autogenerate -m "what changed"`
3. Review the generated file in `db/versions/`
4. Apply it: `python -m alembic upgrade head`
5. Verify in SQLTools or via a check script

---

## Feature Roadmap

- **Phase 1 (Current):** Start/Sit Optimizer — Gridiron Grade (0–100), Matchup Grade (Green/Yellow/Red), Chaos Score
- **Phase 2:** Trade Architect — Monte Carlo simulations for playoff probability impact
- **Phase 3:** Post-Game Autopsy — Expected vs actual points, buy-low candidates
