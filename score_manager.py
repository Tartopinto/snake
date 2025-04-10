import json
import os

SCORE_FILE = "scores.json"
MAX_SCORES = 3

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def save_score(score):
    scores = load_scores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:MAX_SCORES]
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

def get_top_scores():
    return load_scores()
