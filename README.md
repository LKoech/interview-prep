# Interview Prep Coach

A backend-heavy Python application that helps you practice for job interviews. Paste a job description, get tailored questions, practice your answers, and receive structured feedback.

## What It Does

1. **Parses job descriptions** — extracts skill keywords (Python, Docker, Kubernetes, etc.) using regex
2. **Generates tailored questions** — behavioral, technical, and system design questions based on extracted skills
3. **Scores your answers** — evaluates against 5 criteria (concrete examples, metrics, conciseness, relevance, STAR format) with a 1-5 score each
4. **Real-time mock interviews** — WebSocket endpoint that sends questions one at a time and gives instant feedback

## Tech Stack

- **FastAPI** — async REST API with auto-generated Swagger docs
- **Redis** — used as both a primary data store (sessions, questions) and a pub/sub message broker (event bus)
- **Pydantic v2** — data validation and serialization
- **Streamlit** — lightweight frontend for interacting with the API
- **Docker Compose** — multi-service orchestration
- **pytest** — async test suite

## Design Patterns

- **Strategy** — swappable question generation algorithms (`app/strategies/`)
- **Factory** — centralized strategy creation (`app/factories/`)
- **Repository** — abstracts Redis storage behind a clean interface (`app/repositories/`)
- **Observer** — event-driven architecture via Redis pub/sub (`app/events/`)
- **Dependency Injection** — FastAPI's `Depends()` for loose coupling (`app/dependencies.py`)

## Project Structure

```
app/
  main.py              # FastAPI app, lifespan, router registration
  config.py            # Settings via pydantic-settings
  dependencies.py      # DI providers
  models/              # Pydantic models (session, question, feedback)
  routers/             # API endpoints (sessions, questions, feedback, websocket)
  services/            # Business logic (JD parsing, question generation, feedback)
  strategies/          # Strategy pattern (behavioral, technical, system_design)
  factories/           # Factory pattern for strategies
  repositories/        # Redis data access layer
  events/              # Event bus (Redis pub/sub)
tests/                 # pytest test suite
streamlit_app.py       # Lightweight Streamlit UI
```

## How to Run

### 1. Start Redis

```bash
docker-compose up redis -d
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the backend

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Start the Streamlit UI (new terminal)

```bash
streamlit run streamlit_app.py
```

- **Swagger docs:** http://localhost:8000/docs
- **Streamlit UI:** http://localhost:8501

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/sessions/` | Create an interview session |
| GET | `/api/v1/sessions/` | List all sessions |
| GET | `/api/v1/sessions/{id}` | Get a session |
| DELETE | `/api/v1/sessions/{id}` | Delete a session |
| POST | `/api/v1/questions/generate` | Generate questions for a session |
| GET | `/api/v1/questions/{session_id}` | Get questions for a session |
| POST | `/api/v1/feedback/evaluate` | Evaluate an answer |
| WS | `/ws/interview/{session_id}` | Real-time mock interview |

## Running Tests

```bash
pytest
```
