import threading
import psutil

# exe_path -> set of pids
_active_unlocks = {}
_pending_unlocks = set()
_lock = threading.Lock()


def unlock_once(exe_path: str):
    exe_path = exe_path.lower()
    with _lock:
        _pending_unlocks.add(exe_path)


def is_unlocked(exe_path: str, pid: int) -> bool:
    exe_path = exe_path.lower()

    with _lock:
        # Already unlocked exe → allow any instance
        if exe_path in _active_unlocks:
            _active_unlocks[exe_path].add(pid)
            return True

        # First unlock binds exe (not pid)
        if exe_path in _pending_unlocks:
            _pending_unlocks.remove(exe_path)
            _active_unlocks[exe_path] = {pid}
            return True

        return False


def cleanup_dead_processes():
    with _lock:
        dead_exes = []

        for exe, pids in _active_unlocks.items():
            alive = {pid for pid in pids if psutil.pid_exists(pid)}

            if alive:
                _active_unlocks[exe] = alive
            else:
                dead_exes.append(exe)

        for exe in dead_exes:
            del _active_unlocks[exe]