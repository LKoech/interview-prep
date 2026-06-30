from uuid import uuid4

from app.models.question import Question, QuestionType
from app.strategies.base import QuestionStrategy

# Templates map skill categories to behavioral questions
BEHAVIORAL_TEMPLATES = {
    "teamwork": [
        "Tell me about a time you worked with non-technical stakeholders to deliver a feature.",
        "Describe a situation where you had to resolve a disagreement within your team.",
        "How do you handle giving or receiving critical feedback from a teammate?",
    ],
    "autonomy": [
        "Describe a time you took initiative to solve a problem without being asked.",
        "Tell me about a project where you had to work with minimal guidance.",
        "How do you prioritise when there's more work than people to do it?",
    ],
    "ownership": [
        "Tell me about a feature you owned end-to-end from requirements to deployment.",
        "Describe a time you identified and fixed a problem before it affected users.",
        "What's a project you're most proud of and why?",
    ],
    "communication": [
        "How would you explain a complex technical decision to a non-technical audience?",
        "Tell me about a time you had to present findings to senior stakeholders.",
        "Describe how you document your work for other engineers.",
    ],
    "adaptability": [
        "Tell me about a time you had to learn a new technology quickly.",
        "How do you handle ambiguity in requirements?",
        "Describe a situation where priorities shifted mid-project. How did you adapt?",
    ],
}


class BehavioralStrategy(QuestionStrategy):
    """Generates behavioral interview questions based on JD skill signals."""

    def _match_categories(self, skills: list[str]) -> list[str]:
        skill_text = " ".join(skills).lower()
        matched = []
        keyword_map = {
            "teamwork": ["team", "collaborat", "cross-functional", "stakeholder"],
            "autonomy": ["autonomy", "self-driven", "independent", "pragmati"],
            "ownership": ["own", "end-to-end", "deliver", "ship", "production"],
            "communication": ["document", "knowledge sharing", "present"],
            "adaptability": ["fast-paced", "startup", "varied", "flexible"],
        }
        for category, keywords in keyword_map.items():
            if any(kw in skill_text for kw in keywords):
                matched.append(category)
        # Always include ownership and autonomy as baseline
        for default in ["ownership", "autonomy"]:
            if default not in matched:
                matched.append(default)
        return matched

    def generate(self, session_id: str, skills: list[str], count: int) -> list[Question]:
        categories = self._match_categories(skills)
        questions = []
        for category in categories:
            templates = BEHAVIORAL_TEMPLATES.get(category, [])
            for template in templates[:count]:
                questions.append(
                    Question(
                        id=uuid4().hex[:10],
                        session_id=session_id,
                        type=QuestionType.BEHAVIORAL,
                        text=template,
                        skill_tags=[category],
                        difficulty="medium",
                    )
                )
                if len(questions) >= count:
                    break
            if len(questions) >= count:
                break
        return questions[:count]
