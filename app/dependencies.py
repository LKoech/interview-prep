"""Dependency Injection providers — FastAPI's Depends() pattern."""

from fastapi import Depends, Request
from redis.asyncio import Redis

from app.events.bus import EventBus
from app.repositories.question_repo import QuestionRepository
from app.repositories.session_repo import SessionRepository
from app.services.feedback_service import FeedbackService
from app.services.jd_parser import JDParser
from app.services.question_service import QuestionService
from app.strategies.behavioral import BehavioralStrategy
from app.strategies.system_design import SystemDesignStrategy
from app.strategies.technical import TechnicalStrategy


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


def get_event_bus(request: Request) -> EventBus:
    return request.app.state.event_bus


def get_session_repo(redis: Redis = Depends(get_redis)) -> SessionRepository:
    return SessionRepository(redis)


def get_question_repo(redis: Redis = Depends(get_redis)) -> QuestionRepository:
    return QuestionRepository(redis)


def get_jd_parser() -> JDParser:
    return JDParser()


def get_question_service(
    question_repo: QuestionRepository = Depends(get_question_repo),
    jd_parser: JDParser = Depends(get_jd_parser),
    event_bus: EventBus = Depends(get_event_bus),
) -> QuestionService:
    strategies = {
        "behavioral": BehavioralStrategy(),
        "technical": TechnicalStrategy(),
        "system_design": SystemDesignStrategy(),
    }
    return QuestionService(question_repo, jd_parser, strategies, event_bus)


def get_feedback_service() -> FeedbackService:
    return FeedbackService()
