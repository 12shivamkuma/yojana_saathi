
import json
import re
from pathlib import Path

KB_PATH = Path(__file__).resolve().parent.parent / "kb" / "schemes.json"


def load_schemes():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_schemes(user_query):
    schemes = load_schemes()
    query = normalize_text(user_query)

    results = []

    for scheme in schemes:
        score = 0

        name = normalize_text(scheme["name"])

        if name in query:
            score += 20

        for keyword in scheme["keywords"]:
            keyword = normalize_text(keyword)

            if keyword and keyword in query:
                # Give more importance to specific phrases
                score += 2 + (3 * len(keyword.split()))

        if score > 0:
            results.append((score, scheme))

    results.sort(key=lambda item: item[0], reverse=True)

    return [scheme for score, scheme in results]
