import psutil
import time
from gate import trigger_gate
from unlock_state import is_unlocked
from config import CHECK_INTERVAL_MS

def watch(blocked_apps):
    blocked = {app["path"].lower() for app in blocked_apps}

    while True:
        for proc in psutil.process_iter(["exe"]):
            try:
                exe = proc.info["exe"]
                if not exe:
                    continue

                exe_l = exe.lower()

                if exe_l in blocked:
                    if is_unlocked(exe_l):
                        continue  # let it live

                    proc.kill()
                    trigger_gate(exe)
            except Exception:
                pass

        time.sleep(CHECK_INTERVAL_MS / 1000)