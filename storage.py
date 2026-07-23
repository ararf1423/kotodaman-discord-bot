import json
import os

FILE_NAME = "events.json"


def load_events():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_events(events):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)