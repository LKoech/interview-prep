from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class InterviewStage(str, Enum):
    SCREENING = "screening"
    HIRING_MANAGER = "hiring_manager"
    TECHNICAL = "technical"
    SYSTEM_DESIGN = "system_design"


class SessionCreate(BaseModel):
    company: str
    role: str
    jd_text: str
    stage: InterviewStage = InterviewStage.HIRING_MANAGER


class InterviewSession(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:12])
    company: str
    role: str
    jd_text: str
    stage: InterviewStage
    skills_extracted: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
