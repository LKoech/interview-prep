from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI

from app.config import settings
from app.events.bus import EventBus
from app.routers import feedback, questions, sessions, websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage Redis connection pool lifecycle."""
    pool = redis.ConnectionPool.from_url(settings.redis_url)
    app.state.redis = redis.Redis(connection_pool=pool)
    app.state.event_bus = EventBus(app.state.redis)
    await app.state.event_bus.start()
    yield
    await app.state.event_bus.stop()
    await app.state.redis.close()


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(questions.router, prefix="/api/v1/questions", tags=["questions"])
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["feedback"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/health")
async def health():
    return {"status": "ok"}
