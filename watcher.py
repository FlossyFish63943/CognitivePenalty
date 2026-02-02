import psutil
import time
import traceback

from gate import trigger_gate
from unlock_state import is_unlocked, cleanup_dead_processes
from config import CHECK_INTERVAL_MS
from fingerprint import sha256_of_file, get_original_filename
from storage import DATA_PATH, load_blocked_apps


def _build_blocked_sets(apps):
    blocked_hashes = set()
    blocked_original_names = set()

    for app in apps:
        if app.get("sha256"):
            blocked_hashes.add(app["sha256"].lower())

        if app.get("original_name"):
            blocked_original_names.add(app["original_name"].lower())

    return blocked_hashes, blocked_original_names


def _blocked_apps_mtime():
    if DATA_PATH.exists():
        return DATA_PATH.stat().st_mtime
    return None


def watch(enabled_flag):
    print("[Watcher] started")

    blocked_apps = load_blocked_apps()
    blocked_hashes, blocked_original_names = _build_blocked_sets(blocked_apps)
    last_mtime = _blocked_apps_mtime()

    print("[Watcher] hashes:", blocked_hashes)
    print("[Watcher] original names:", blocked_original_names)

    while True:
        try:
            if not enabled_flag.is_set():
                time.sleep(0.2)
                continue

            print("[Watcher] tick")
            cleanup_dead_processes()

            current_mtime = _blocked_apps_mtime()
            if current_mtime != last_mtime:
                blocked_apps = load_blocked_apps()
                blocked_hashes, blocked_original_names = _build_blocked_sets(blocked_apps)
                last_mtime = current_mtime
                print("[Watcher] updated hashes:", blocked_hashes)
                print("[Watcher] updated original names:", blocked_original_names)

            for proc in psutil.process_iter(["exe"]):
                try:
                    exe = proc.info["exe"]
                    if not exe:
                        continue

                    exe_l = exe.lower()

                    if is_unlocked(exe_l, proc.pid):
                        print("ALLOW", exe_l, proc.pid)
                        continue

                    # 🔹 rename detection
                    original = get_original_filename(exe_l)
                    if original and original.lower() in blocked_original_names:
                        print("[BLOCKED] rename match:", exe)
                        proc.kill()
                        trigger_gate(exe)
                        continue

                    # 🔹 hash detection
                    if blocked_hashes:
                        sha = sha256_of_file(exe_l, cache=True)
                        if sha and sha.lower() in blocked_hashes:
                            print("[BLOCKED] hash match:", exe)
                            proc.kill()
                            trigger_gate(exe)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # ✅ correct sleep
            time.sleep(CHECK_INTERVAL_MS / 1000)

        except Exception:
            print("[Watcher] CRASH — restarting loop")
            traceback.print_exc()
            time.sleep(1)
