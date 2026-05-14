# Local Setup

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker Desktop
- PostgreSQL client or database viewer is helpful but optional

## Start infrastructure

From the repository root:

```bash
docker-compose up -d
```

This starts:

- PostgreSQL on port `5432`
- Redis on port `6379`

## Backend setup

From the repository root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python -m alembic upgrade head
```

Start the backend:

```bash
python -m uvicorn app.main:app --reload
```

Backend runs at:

```txt
http://localhost:8000
```

API docs:

```txt
http://localhost:8000/docs
```

Health check:

```txt
http://localhost:8000/health
```

## Backend environment variables

Create `backend/.env` locally.

Expected keys:

```txt
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gridiron
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
CLERK_SECRET_KEY=
```

Do not commit real `.env` values.

## Seed player data

After applying migrations and starting Postgres, run:

```bash
cd backend
python -m scripts.seed_players
```

The seed script fetches NFL players from Sleeper and inserts relevant skill positions.

## Create the dev user

Current roster and lineup routes use `DEV_USER_ID = 1`, so local development needs a user with id 1.

The uploaded SQL session included this development insert:

```sql
INSERT INTO users (clerk_id, email, username)
VALUES ('dev_user', 'dev@gridironlabs.com', 'DevUser');
```

Run this manually after migrations if no user exists.

## Frontend setup

From the repository root:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```txt
http://localhost:5173
```

## Frontend environment variables

Create `frontend/.env.local` locally.

Expected key:

```txt
VITE_API_URL=http://localhost:8000
```

Future auth key from the main README:

```txt
VITE_CLERK_PUBLISHABLE_KEY=
```

## Common development commands

### Frontend

```bash
npm run dev
npm run build
npm run lint
npm run preview
```

### Backend

```bash
python -m uvicorn app.main:app --reload
python -m alembic upgrade head
python -m alembic revision --autogenerate -m "describe change"
python -m pytest
```

## Troubleshooting

### Frontend cannot reach backend

Check:

- backend is running on port 8000;
- `VITE_API_URL` is set to `http://localhost:8000`;
- CORS allows `http://localhost:5173` in `backend/app/main.py`.

### Roster or lineup returns empty/unexpected data

Check:

- dev user with id 1 exists;
- players were seeded;
- roster rows point to `user_id = 1`.

### Alembic cannot connect

Check:

- Docker Postgres is running;
- `DATABASE_URL` is set;
- `backend/db/env.py` reads `settings.database_url`.

## Security note

The uploaded ZIP contained `.env` files. This setup guide documents only variable names and safe example values. Do not commit real environment secrets.
