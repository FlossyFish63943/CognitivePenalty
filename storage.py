import json
from pathlib import Path

from fingerprint import sha256_of_file, get_original_filename

DATA_PATH = Path("data/blocked_apps.json")


def load_blocked_apps():
    if not DATA_PATH.exists():
        return []

    apps = json.loads(DATA_PATH.read_text())
    changed = False

    for app in apps:
        path = app.get("path")
        if not path:
            continue

        # Add SHA-256 if missing
        if "sha256" not in app or not app["sha256"]:
            sha = sha256_of_file(path)
            if sha:
                app["sha256"] = sha
                changed = True

        # Add OriginalFilename if missing
        if "original_name" not in app or not app["original_name"]:
            original = get_original_filename(path)
            if original:
                app["original_name"] = original
                changed = True

    if changed:
        save_blocked_apps(apps)

    return apps


def save_blocked_apps(apps):
    DATA_PATH.parent.mkdir(exist_ok=True)
    DATA_PATH.write_text(json.dumps(apps, indent=2))