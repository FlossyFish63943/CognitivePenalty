import time

UNLOCKED = {}

COOLDOWN_SECONDS = 30 * 60  # 30 minutes

def unlock(app_path):
    UNLOCKED[app_path.lower()] = time.time() + COOLDOWN_SECONDS

def is_unlocked(app_path):
    expiry = UNLOCKED.get(app_path.lower())
    if not expiry:
        return False

    if time.time() > expiry:
        del UNLOCKED[app_path.lower()]
        return False

    return True