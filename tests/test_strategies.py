from app.strategies.behavioral import BehavioralStrategy
from app.strategies.system_design import SystemDesignStrategy
from app.strategies.technical import TechnicalStrategy

SKILLS = ["python", "async", "microservices", "redis", "event_driven", "autonomy", "team_player"]


def test_behavioral_generates_correct_count():
    strategy = BehavioralStrategy()
    questions = strategy.generate("test-session", SKILLS, count=3)
    assert len(questions) == 3
    assert all(q.type == "behavioral" for q in questions)


def test_behavioral_has_ownership_by_default():
    strategy = BehavioralStrategy()
    questions = strategy.generate("test-session", ["unrelated_skill"], count=3)
    tags = [tag for q in questions for tag in q.skill_tags]
    assert "ownership" in tags or "autonomy" in tags


def test_technical_generates_correct_count():
    strategy = TechnicalStrategy()
    questions = strategy.generate("test-session", SKILLS, count=5)
    assert len(questions) == 5
    assert all(q.type == "technical" for q in questions)


def test_technical_matches_python_skills():
    strategy = TechnicalStrategy()
    questions = strategy.generate("test-session", ["python"], count=2)
    tags = [tag for q in questions for tag in q.skill_tags]
    assert "python" in tags


def test_system_design_generates_questions():
    strategy = SystemDesignStrategy()
    questions = strategy.generate("test-session", SKILLS, count=3)
    assert len(questions) <= 3
    assert all(q.type == "system_design" for q in questions)


def test_system_design_ranks_by_relevance():
    strategy = SystemDesignStrategy()
    questions = strategy.generate("test-session", ["event_driven", "streaming"], count=2)
    # First question should have event-related tags
    if questions:
        assert any("event" in tag for tag in questions[0].skill_tags)
