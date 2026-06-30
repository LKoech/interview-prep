from uuid import uuid4

from app.models.question import Question, QuestionType
from app.strategies.base import QuestionStrategy

TECHNICAL_TEMPLATES = {
    "python": [
        "What's the difference between asyncio.gather and asyncio.wait? When would you use each?",
        "Explain Python's GIL. How does it affect async vs threaded code?",
        "How would you structure a large Python project to keep it maintainable?",
        "What are Python descriptors and when would you use them?",
    ],
    "async": [
        "Walk me through how async/await works in Python under the hood.",
        "How would you handle a mix of CPU-bound and IO-bound tasks in an async application?",
        "What are the trade-offs between asyncio, threading, and multiprocessing in Python?",
    ],
    "rest_api": [
        "How do you design RESTful API versioning for a production service?",
        "What's your approach to API error handling and status codes?",
        "How do you handle pagination and filtering in a REST API?",
    ],
    "redis": [
        "What Redis data structures would you use for a real-time leaderboard?",
        "Explain Redis pub/sub vs Redis Streams. When would you choose each?",
        "How do you handle cache invalidation in a Redis-backed system?",
    ],
    "microservices": [
        "What are the advantages and disadvantages of microservices architecture?",
        "How do you handle distributed transactions across microservices?",
        "What's your approach to service discovery and communication between services?",
    ],
    "event_driven": [
        "Explain event sourcing. When is it a good fit vs a bad fit?",
        "How would you design an event-driven pipeline for processing trading data?",
        "What strategies do you use to handle message ordering and deduplication?",
    ],
    "docker": [
        "How do you optimise Docker images for production?",
        "Explain multi-stage Docker builds and when you'd use them.",
    ],
    "testing": [
        "What's your testing strategy for async Python code?",
        "How do you test microservices in isolation vs integration?",
    ],
}


class TechnicalStrategy(QuestionStrategy):
    """Generates technical questions matched to JD skills."""

    SKILL_KEYWORD_MAP = {
        "python": ["python"],
        "async": ["async", "asynchronous"],
        "rest_api": ["rest", "api", "fastapi", "endpoint"],
        "redis": ["redis"],
        "microservices": ["microservice"],
        "event_driven": ["event", "streaming", "kafka", "rabbitmq"],
        "docker": ["docker", "kubernetes", "container"],
        "testing": ["test", "coverage", "quality"],
    }

    def _match_skills(self, skills: list[str]) -> list[str]:
        skill_text = " ".join(skills).lower()
        matched = []
        for category, keywords in self.SKILL_KEYWORD_MAP.items():
            if any(kw in skill_text for kw in keywords):
                matched.append(category)
        if not matched:
            matched = ["python", "rest_api"]
        return matched

    def generate(self, session_id: str, skills: list[str], count: int) -> list[Question]:
        categories = self._match_skills(skills)
        questions = []
        # Round-robin across matched categories
        cat_index = 0
        used_templates: set[str] = set()
        while len(questions) < count:
            category = categories[cat_index % len(categories)]
            templates = TECHNICAL_TEMPLATES.get(category, [])
            for template in templates:
                if template not in used_templates:
                    used_templates.add(template)
                    questions.append(
                        Question(
                            id=uuid4().hex[:10],
                            session_id=session_id,
                            type=QuestionType.TECHNICAL,
                            text=template,
                            skill_tags=[category],
                            difficulty="medium",
                        )
                    )
                    break
            cat_index += 1
            # Safety: break if we've exhausted all templates
            if cat_index > len(categories) * 5:
                break
        return questions[:count]
