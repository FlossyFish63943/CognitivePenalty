from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from config import THEME

class GateDialog(QDialog):
    def __init__(self, question, answer):
        super().__init__()
        self.answer = answer

        self.setWindowTitle("CognitivePenalty")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()

        label = QLabel(question)
        label.setStyleSheet(f"color: {THEME['fg']}; font-size: 16px;")
        label.setWordWrap(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Final answer")
        self.input.setStyleSheet("font-size: 14px;")

        btn = QPushButton("Submit")
        btn.clicked.connect(self.check)

        layout.addWidget(label)
        layout.addWidget(self.input)
        layout.addWidget(btn)

        self.setStyleSheet(f"background-color: {THEME['bg']};")
        self.setLayout(layout)

    def check(self):
        if self.input.text().strip() == self.answer:
            self.accept()
        else:
            self.input.clear()