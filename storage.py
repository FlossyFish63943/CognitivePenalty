import json
from pathlib import Path

DATA_PATH = Path("data/blocked_apps.json")

def load_blocked_apps():
    if not DATA_PATH.exists():
        return []
    return json.loads(DATA_PATH.read_text())

def save_blocked_apps(apps):
    DATA_PATH.parent.mkdir(exist_ok=True)
    DATA_PATH.write_text(json.dumps(apps, indent=2))