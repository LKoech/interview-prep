from enum import Enum

from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    SYSTEM_DESIGN = "system_design"


class Question(BaseModel):
    id: str
    session_id: str
    type: QuestionType
    text: str
    skill_tags: list[str] = Field(default_factory=list)
    suggested_experience: list[str] = Field(default_factory=list)
    difficulty: str = "medium"


class QuestionGenerateRequest(BaseModel):
    session_id: str
    types: list[QuestionType] = Field(
        default_factory=lambda: [
            QuestionType.BEHAVIORAL,
            QuestionType.TECHNICAL,
            QuestionType.SYSTEM_DESIGN,
        ]
    )
    count_per_type: int = 3
