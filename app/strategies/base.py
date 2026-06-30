"""Strategy pattern: abstract base for question generation strategies.

Each strategy knows how to generate questions of a specific type
(behavioral, technical, system design) given extracted skills from a JD.
The QuestionService selects and delegates to strategies at runtime.
"""

from abc import ABC, abstractmethod

from app.models.question import Question


class QuestionStrategy(ABC):

    @abstractmethod
    def generate(self, session_id: str, skills: list[str], count: int) -> list[Question]:
        ...
