from app.services.feedback_service import FeedbackService

service = FeedbackService()


def test_detects_concrete_example():
    question = "Tell me about a project you owned."
    answer = (
        "At Goldman Sachs, I owned the delivery of production features for "
        "financial applications used by 300+ users. During my time there, I "
        "managed requirements refinement, UAT coordination, and deployment."
    )
    feedback = service.evaluate(question, answer)
    assert feedback.has_concrete_example.score >= 3


def test_detects_metrics():
    question = "What impact have you had?"
    answer = (
        "I built 10+ RESTful APIs with Spring Boot, contributing to a 9% "
        "reduction in response time. I also maintained 96% test coverage."
    )
    feedback = service.evaluate(question, answer)
    assert feedback.has_metric.score >= 3


def test_detects_no_metrics():
    question = "What impact have you had?"
    answer = "I worked on some APIs and improved things."
    feedback = service.evaluate(question, answer)
    assert feedback.has_metric.score <= 2


def test_conciseness_good_length():
    question = "Tell me about yourself."
    answer = " ".join(["word"] * 100)
    feedback = service.evaluate(question, answer)
    assert feedback.is_concise.score >= 3


def test_conciseness_too_long():
    question = "Tell me about yourself."
    answer = " ".join(["word"] * 350)
    feedback = service.evaluate(question, answer)
    assert feedback.is_concise.score <= 2


def test_star_format_detected():
    question = "Tell me about a challenge."
    answer = (
        "When I was at Goldman Sachs, I needed to evaluate DynamoDB vs our "
        "existing database. I led the analysis independently, comparing "
        "performance and cost. I built a structured comparison and presented "
        "it to global stakeholders. This resulted in the team adopting "
        "DynamoDB, achieving alignment across engineering."
    )
    feedback = service.evaluate(question, answer)
    assert feedback.uses_star_format.score >= 3


def test_overall_score_range():
    question = "Any question"
    answer = "Short answer."
    feedback = service.evaluate(question, answer)
    assert 1.0 <= feedback.overall_score <= 5.0
