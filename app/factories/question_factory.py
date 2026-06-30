"""Factory pattern: creates the right strategy based on question type.

The service layer asks the factory for a strategy by type name,
without knowing which concrete class it gets back.
"""

from app.models.question import QuestionType
from app.strategies.base import QuestionStrategy
from app.strategies.behavioral import BehavioralStrategy
from app.strategies.system_design import SystemDesignStrategy
from app.strategies.technical import TechnicalStrategy

_STRATEGY_MAP: dict[QuestionType, type[QuestionStrategy]] = {
    QuestionType.BEHAVIORAL: BehavioralStrategy,
    QuestionType.TECHNICAL: TechnicalStrategy,
    QuestionType.SYSTEM_DESIGN: SystemDesignStrategy,
}


def create_strategy(question_type: QuestionType) -> QuestionStrategy:
    strategy_class = _STRATEGY_MAP.get(question_type)
    if strategy_class is None:
        raise ValueError(f"Unknown question type: {question_type}")
    return strategy_class()
