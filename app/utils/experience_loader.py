"""Loads experience .md files and maps achievements to question categories."""

import re
from pathlib import Path


def load_experience_files(directory: str) -> dict[str, str]:
    """Load all .md files from a directory into a dict of {filename: content}."""
    path = Path(directory)
    if not path.exists():
        return {}
    return {
        f.stem: f.read_text(encoding="utf-8")
        for f in path.glob("*.md")
    }


def extract_achievement_ids(content: str) -> list[dict[str, str]]:
    """Extract achievement IDs and their bullet variants from experience markdown."""
    achievements = []
    blocks = re.split(r"### Achievement\s+", content)

    for block in blocks[1:]:  # skip first split (before any achievement)
        lines = block.strip().split("\n")
        header = lines[0] if lines else ""

        # Extract ID (e.g., "GS1", "P4", "I2")
        id_match = re.match(r"(\w+):", header)
        achievement_id = id_match.group(1) if id_match else "unknown"

        # Extract title
        title = header.split(":", 1)[1].strip() if ":" in header else header

        # Extract 1L bullet
        bullet_1l = ""
        for line in lines:
            if "Resume-1L" in line:
                bullet_1l = line.split(":**", 1)[1].strip() if ":**" in line else ""
                break

        achievements.append({
            "id": achievement_id,
            "title": title,
            "bullet": bullet_1l,
        })

    return achievements
