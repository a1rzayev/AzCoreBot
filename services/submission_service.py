import json
from datetime import datetime

FILE_PATH = "data/submissions.json"

def save_submission(data):
    data["timestamp"] = str(datetime.now())

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        submissions = []

    submissions.append(data)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=4)