import logging
from typing import Any

logger = logging.getLogger(__name__)


async def on_session_created(data: dict[str, Any]) -> None:
    logger.info(f"Session created: {data.get('session_id')} for {data.get('company')}")


async def on_questions_generated(data: dict[str, Any]) -> None:
    count = data.get("count", 0)
    session_id = data.get("session_id")
    logger.info(f"Generated {count} questions for session {session_id}")
