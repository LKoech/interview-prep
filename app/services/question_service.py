from app.events.bus import EventBus
from app.models.question import Question, QuestionType
from app.repositories.question_repo import QuestionRepository
from app.services.jd_parser import JDParser
from app.strategies.base import QuestionStrategy


class QuestionService:
    """Orchestrates question generation using strategies and the event bus."""

    def __init__(
        self,
        question_repo: QuestionRepository,
        jd_parser: JDParser,
        strategies: dict[str, QuestionStrategy],
        event_bus: EventBus,
    ):
        self._repo = question_repo
        self._parser = jd_parser
        self._strategies = strategies
        self._event_bus = event_bus

    async def generate_for_session(
        self,
        session_id: str,
        jd_text: str,
        types: list[QuestionType],
        count_per_type: int = 3,
    ) -> list[Question]:
        skills = self._parser.extract_skills(jd_text)
        all_questions: list[Question] = []

        for q_type in types:
            strategy = self._strategies.get(q_type.value)
            if strategy is None:
                continue
            questions = strategy.generate(session_id, skills, count_per_type)
            for q in questions:
                await self._repo.save_question(q)
                all_questions.append(q)

        await self._event_bus.publish(
            "questions_generated",
            {"session_id": session_id, "count": len(all_questions)},
        )

        return all_questions

    async def get_session_questions(self, session_id: str) -> list[Question]:
        return await self._repo.get_by_session(session_id)
