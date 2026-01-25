from ui.gate_dialog import GateDialog
from math_engine import generate_question
from unlock_state import unlock_once
from PySide6.QtWidgets import QApplication
import sys
import os

def trigger_gate(app_path):
    app = QApplication.instance() or QApplication(sys.argv)

    q = generate_question()
    dlg = GateDialog(q["question"], q["answer"])

    if dlg.exec():
        unlock_once(app_path)
        os.startfile(app_path)  # Windows-safe