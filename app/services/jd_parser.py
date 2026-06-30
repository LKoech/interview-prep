"""Parses a job description and extracts skill keywords."""

import re


# Skill categories and their keyword patterns
SKILL_PATTERNS = {
    "python": r"\bpython\b",
    "async": r"\basync(?:hronous)?\b",
    "fastapi": r"\bfastapi\b",
    "django": r"\bdjango\b",
    "rest_api": r"\brest(?:ful)?\s*api\b",
    "redis": r"\bredis\b",
    "microservices": r"\bmicroservice",
    "event_driven": r"\bevent[\s-]driven\b",
    "streaming": r"\b(?:kafka|rabbitmq|redis\s*streams?)\b",
    "websocket": r"\bwebsocket",
    "kubernetes": r"\bkubernetes\b|\bk8s\b",
    "docker": r"\bdocker\b",
    "ci_cd": r"\bci/?cd\b",
    "testing": r"\btest(?:ing|s)?\b",
    "aws": r"\baws\b",
    "terraform": r"\bterraform\b",
    "sql": r"\bsql\b",
    "graphql": r"\bgraphql\b",
    "react": r"\breact\b",
    "typescript": r"\btypescript\b",
    "low_latency": r"\blow[\s-]latency\b",
    "observability": r"\b(?:grafana|datadog|sentry|observability)\b",
    "agile": r"\bagile\b",
    "autonomy": r"\bautonomy\b|\bself[\s-]driven\b",
    "team_player": r"\bteam\s*player\b|\bcollaborat",
    "documentation": r"\bdocumentation\b|\bknowledge\s*sharing\b",
}


class JDParser:
    """Extracts structured skill tags from raw JD text."""

    def extract_skills(self, jd_text: str) -> list[str]:
        text_lower = jd_text.lower()
        matched = []
        for skill, pattern in SKILL_PATTERNS.items():
            if re.search(pattern, text_lower):
                matched.append(skill)
        return matched

    def extract_company_info(self, jd_text: str) -> dict[str, str]:
        lines = jd_text.strip().split("\n")
        return {
            "raw_first_line": lines[0] if lines else "",
            "word_count": str(len(jd_text.split())),
        }
