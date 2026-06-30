import re

from app.models.feedback import AnswerFeedback, FeedbackCriteria


class FeedbackService:
    """Evaluates user answers against interview best practices."""

    METRIC_PATTERNS = [
        r"\d+%",
        r"\d+\+?\s*(?:users?|teams?|apis?|endpoints?|features?|services?)",
        r"(?:reduced|improved|increased|decreased)\s+(?:by\s+)?\d+",
    ]

    STAR_KEYWORDS = {
        "situation": ["when", "at", "during", "while"],
        "task": ["needed to", "responsible for", "had to", "goal was"],
        "action": ["i built", "i designed", "i led", "i implemented", "i created"],
        "result": ["resulted in", "which led to", "achieving", "delivered", "shipped"],
    }

    def evaluate(self, question_text: str, answer_text: str) -> AnswerFeedback:
        answer_lower = answer_text.lower()
        words = answer_text.split()

        has_example = self._check_concrete_example(answer_lower)
        has_metric = self._check_metrics(answer_text)
        is_concise = self._check_conciseness(words)
        answers_q = self._check_relevance(question_text.lower(), answer_lower)
        uses_star = self._check_star(answer_lower)

        criteria = [has_example, has_metric, is_concise, answers_q, uses_star]
        overall = sum(c.score for c in criteria) / len(criteria)

        suggestion = self._build_suggestion(
            has_example, has_metric, is_concise, answers_q, uses_star
        )

        return AnswerFeedback(
            question_id="",
            has_concrete_example=has_example,
            has_metric=has_metric,
            is_concise=is_concise,
            answers_the_question=answers_q,
            uses_star_format=uses_star,
            overall_score=round(overall, 1),
            suggestion=suggestion,
        )

    def _check_concrete_example(self, answer: str) -> FeedbackCriteria:
        example_signals = [
            "at goldman", "at octopus", "at my", "in my",
            "for example", "for instance", "one time", "i remember",
            "last year", "recently", "during my",
        ]
        matches = sum(1 for s in example_signals if s in answer)
        if matches >= 2:
            return FeedbackCriteria(score=5, comment="Strong concrete example with context.")
        if matches == 1:
            return FeedbackCriteria(score=3, comment="Has an example but could add more specific context.")
        return FeedbackCriteria(score=1, comment="No concrete example. Use a real situation from your experience.")

    def _check_metrics(self, answer: str) -> FeedbackCriteria:
        matches = sum(1 for p in self.METRIC_PATTERNS if re.search(p, answer, re.IGNORECASE))
        if matches >= 2:
            return FeedbackCriteria(score=5, comment="Great use of multiple metrics.")
        if matches == 1:
            return FeedbackCriteria(score=3, comment="One metric found. Try to add a second for more impact.")
        return FeedbackCriteria(score=1, comment="No metrics. Quantify your impact (users, %, time saved).")

    def _check_conciseness(self, words: list[str]) -> FeedbackCriteria:
        count = len(words)
        if 50 <= count <= 200:
            return FeedbackCriteria(score=5, comment=f"Good length ({count} words).")
        if 30 <= count < 50:
            return FeedbackCriteria(score=3, comment=f"A bit short ({count} words). Add more detail.")
        if 200 < count <= 300:
            return FeedbackCriteria(score=3, comment=f"Slightly long ({count} words). Tighten it up.")
        if count > 300:
            return FeedbackCriteria(score=1, comment=f"Too long ({count} words). Keep to 2 minutes max.")
        return FeedbackCriteria(score=2, comment=f"Very short ({count} words). Expand your answer.")

    def _check_relevance(self, question: str, answer: str) -> FeedbackCriteria:
        q_keywords = set(question.split()) - {
            "what", "how", "why", "when", "tell", "me", "about", "a", "the",
            "you", "your", "do", "did", "have", "would", "describe", "time",
        }
        matches = sum(1 for kw in q_keywords if kw in answer)
        ratio = matches / max(len(q_keywords), 1)
        if ratio >= 0.4:
            return FeedbackCriteria(score=5, comment="Answer is well-aligned with the question.")
        if ratio >= 0.2:
            return FeedbackCriteria(score=3, comment="Partially relevant. Tie your answer back to the question.")
        return FeedbackCriteria(score=1, comment="Answer seems off-topic. Re-read the question and address it directly.")

    def _check_star(self, answer: str) -> FeedbackCriteria:
        found = []
        for component, keywords in self.STAR_KEYWORDS.items():
            if any(kw in answer for kw in keywords):
                found.append(component)
        if len(found) >= 4:
            return FeedbackCriteria(score=5, comment="Excellent STAR structure.")
        if len(found) >= 2:
            missing = set(self.STAR_KEYWORDS.keys()) - set(found)
            return FeedbackCriteria(score=3, comment=f"Partial STAR. Missing: {', '.join(missing)}.")
        return FeedbackCriteria(score=1, comment="No STAR structure detected. Frame as Situation, Task, Action, Result.")

    def _build_suggestion(self, *criteria: FeedbackCriteria) -> str:
        weakest = min(criteria, key=lambda c: c.score)
        return f"Focus on improving: {weakest.comment}"
