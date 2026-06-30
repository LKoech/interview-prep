from app.services.jd_parser import JDParser

SAMPLE_JD = """
We are seeking a software engineer to join the core engineering team.
Advanced-level Python. Asynchronous Python. Microservices. REST APIs.
Event driven architectures. Redis Streams, Kafka. WebSockets. Kubernetes.
FastAPI for RESTful microservices. Docker. CI/CD. Grafana, Datadog, Sentry.
Autonomy and pragmatism. Team player mindset. Documentation and knowledge sharing.
"""


def test_extracts_python():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "python" in skills


def test_extracts_async():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "async" in skills


def test_extracts_fastapi():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "fastapi" in skills


def test_extracts_redis():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "redis" in skills


def test_extracts_microservices():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "microservices" in skills


def test_extracts_event_driven():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "event_driven" in skills


def test_extracts_kubernetes():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "kubernetes" in skills


def test_extracts_observability():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "observability" in skills


def test_extracts_autonomy():
    parser = JDParser()
    skills = parser.extract_skills(SAMPLE_JD)
    assert "autonomy" in skills


def test_empty_jd_returns_empty():
    parser = JDParser()
    skills = parser.extract_skills("")
    assert skills == []
