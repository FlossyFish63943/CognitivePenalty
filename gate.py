import os
import sys

from math_engine import generate_question
from unlock_state import unlock_once


def _is_headless():
    if os.environ.get("CP_HEADLESS") == "1":
        return True
    if sys.platform == "win32":
        return False
    return not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))

def trigger_gate(app_path):
    if _is_headless():
        print("[Gate] Headless mode enabled; skipping UI prompt.")
        return

    from PySide6.QtWidgets import QApplication
    from ui.gate_dialog import GateDialog

    app = QApplication.instance() or QApplication(sys.argv)

    q = generate_question()
    dlg = GateDialog(q["question"], q["answer"])

    if dlg.exec():
        unlock_once(app_path)
        os.startfile(app_path)  # Windows-safe
