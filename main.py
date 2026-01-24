import threading
from watcher import watch
from storage import load_blocked_apps

def main():
    apps = load_blocked_apps()
    t = threading.Thread(target=watch, args=(apps,), daemon=True)
    t.start()

    import time
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()