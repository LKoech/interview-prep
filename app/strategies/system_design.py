from uuid import uuid4

from app.models.question import Question, QuestionType
from app.strategies.base import QuestionStrategy

SYSTEM_DESIGN_TEMPLATES = [
    {
        "text": "Design a real-time energy trading data pipeline that processes market prices and triggers automated trades.",
        "tags": ["event_driven", "streaming", "low_latency"],
        "difficulty": "hard",
    },
    {
        "text": "Design a platform that allows domain teams to deploy event-driven microservices with zero overhead.",
        "tags": ["microservices", "platform", "developer_experience"],
        "difficulty": "hard",
    },
    {
        "text": "Design a WebSocket-based system for pushing live trading updates to a dashboard.",
        "tags": ["websocket", "real_time", "frontend"],
        "difficulty": "medium",
    },
    {
        "text": "Design a caching layer for a high-throughput API that needs sub-100ms response times.",
        "tags": ["redis", "caching", "performance"],
        "difficulty": "medium",
    },
    {
        "text": "Design a notification system that alerts traders when battery prices cross configurable thresholds.",
        "tags": ["event_driven", "pub_sub", "microservices"],
        "difficulty": "medium",
    },
    {
        "text": "How would you migrate a monolithic trading application to microservices without downtime?",
        "tags": ["microservices", "migration", "reliability"],
        "difficulty": "hard",
    },
]


class SystemDesignStrategy(QuestionStrategy):
    """Generates system design questions relevant to the role."""

    def generate(self, session_id: str, skills: list[str], count: int) -> list[Question]:
        skill_text = " ".join(skills).lower()

        # Score templates by how many tags match the JD skills
        scored = []
        for template in SYSTEM_DESIGN_TEMPLATES:
            score = sum(1 for tag in template["tags"] if tag in skill_text)
            scored.append((score, template))
        scored.sort(key=lambda x: x[0], reverse=True)

        questions = []
        for _, template in scored[:count]:
            questions.append(
                Question(
                    id=uuid4().hex[:10],
                    session_id=session_id,
                    type=QuestionType.SYSTEM_DESIGN,
                    text=template["text"],
                    skill_tags=template["tags"],
                    difficulty=template["difficulty"],
                )
            )
        return questions
