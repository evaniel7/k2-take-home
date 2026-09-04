# Decision Queue

A web application for managing product requests and recording decisions.

## Quick Start

### Prerequisites
- Docker and Docker Compose

### Initialize from clean checkout
```bash
docker-compose up --build
```

Sample data is automatically loaded on first startup (14 requests across all statuses).

### Manually re-seed data
```bash
docker-compose exec backend python seed_data.py
```

### Access the application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Run tests
```bash
# Run backend tests
docker-compose exec backend pytest

# Or run locally (requires Python 3.11+)
cd backend
pip install -r requirements.txt
pytest -v
```

### Reset local data
```bash
docker-compose down -v
docker-compose up --build
```

---

## Completed Requirements

### Functional
- [x] Create a request with title, problem statement, expected impact, and urgency
- [x] View all requests in a queue
- [x] Filter and sort the queue by status and urgency
- [x] Open a request and record a decision (accept, defer, decline)
- [x] Add a reason for the decision
- [x] See the current state of the queue

### Non-functional
- [x] Runs locally with Docker Compose
- [x] PostgreSQL database with persistence
- [x] Database migrations (Alembic)
- [x] Input validation with useful error messages
- [x] Automated tests for core workflow (pytest)

---

## Known Gaps

- No pagination for large request lists
- No search functionality
- No bulk operations
- Frontend tests not implemented

---

## Key Technical Decisions

1. **FastAPI + React**: FastAPI provides automatic OpenAPI docs, request validation, and async support. React with TypeScript gives type safety on the frontend.

2. **Decision-based status model**: Status values (`new`, `accepted`, `deferred`, `declined`) directly map to the decision workflow rather than a generic workflow state. Declined requests serve as "archived" items.

3. **SQLite for tests**: Using in-memory SQLite for pytest allows fast, isolated tests without needing a test PostgreSQL instance.

---

## Project Structure

```
.
├── docker-compose.yml
├── frontend/                 # React + TypeScript
│   ├── src/
│   │   ├── api/             # API client
│   │   ├── pages/           # Page components
│   │   └── types.ts         # TypeScript types
│   └── Dockerfile
├── backend/                  # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── routers/         # API routes
│   ├── migrations/          # Alembic migrations
│   └── tests/               # pytest tests
└── README.md
```

---

## Time Spent

50 min Wednesday 9/2/26
1 hr 2 min September 9/3/26
**1 hr 52 min Total Time Spent**

---
