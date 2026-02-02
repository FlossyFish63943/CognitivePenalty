import os
import sys
import threading
import time

from watcher import watch


def _is_headless():
    if os.environ.get("CP_HEADLESS") == "1":
        return True
    if sys.platform == "win32":
        return False
    return not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def main():
    enabled_flag = threading.Event()
    enabled_flag.set()  # start enabled

    def watch_wrapper():
        watch(enabled_flag)

    t = threading.Thread(target=watch_wrapper, daemon=True)
    t.start()

    if _is_headless():
        if os.environ.get("CP_HEADLESS_TEST") == "1":
            time.sleep(float(os.environ.get("CP_HEADLESS_TEST_SECONDS", "0.2")))
            return
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("CognitivePenalty exiting...")
        return

    from PySide6.QtWidgets import QApplication
    from tray import TrayController
    from ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    main_window = MainWindow()
    tray = TrayController()

    def handle_toggle(state):
        if state:
            enabled_flag.set()
        else:
            enabled_flag.clear()

    tray.toggle_requested.connect(handle_toggle)
    tray.open_settings_requested.connect(main_window.show)
    tray.quit_requested.connect(app.quit)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
