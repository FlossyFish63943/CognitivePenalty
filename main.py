import threading
import time

from watcher import watch
from storage import load_blocked_apps


def main():
    apps = load_blocked_apps()

    # THIS is the correct type
    enabled_flag = threading.Event()
    enabled_flag.set()  # start enabled

    def watch_wrapper():
        watch(apps, enabled_flag)

    t = threading.Thread(target=watch_wrapper, daemon=True)
    t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("CognitivePenalty exiting...")


if __name__ == "__main__":
    main()