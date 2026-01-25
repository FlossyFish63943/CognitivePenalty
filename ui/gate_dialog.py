from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QPoint,
    QEasingCurve,
    QTimer,
)
from config import THEME


class GateDialog(QDialog):
    def __init__(self, question, answer):
        super().__init__()
        self.answer = answer

        self.setWindowTitle("CognitivePenalty")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self._shake_anim = None
        self._shake_base_pos = None
        self._is_shaking = False

        layout = QVBoxLayout()

        label = QLabel(question)
        label.setStyleSheet(f"color: {THEME['fg']}; font-size: 16px;")
        label.setWordWrap(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Final answer")
        self.input.setStyleSheet("font-size: 14px;")
        self.input.returnPressed.connect(self.check)

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
            self.input.setStyleSheet(
                f"""
                QLineEdit {{
                    font-size: 14px;
                    border: 2px solid {THEME['danger']};
                }}
                """
            )

            self.input.clear()
            self.shake()

            QTimer.singleShot(400, self.reset_input_style)

    def reset_input_style(self):
        self.input.setStyleSheet("font-size: 14px;")

    def shake(self):
        if self._is_shaking:
            return  # prevent stacking

        self._is_shaking = True

        if self._shake_base_pos is None:
            self._shake_base_pos = self.pos()

        base = self._shake_base_pos
        offset = 10

        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(300)
        anim.setEasingCurve(QEasingCurve.OutQuad)

        anim.setKeyValueAt(0.0, base)
        anim.setKeyValueAt(0.1, base + QPoint(-offset, 0))
        anim.setKeyValueAt(0.2, base + QPoint(offset, 0))
        anim.setKeyValueAt(0.3, base + QPoint(-offset, 0))
        anim.setKeyValueAt(0.4, base + QPoint(offset, 0))
        anim.setKeyValueAt(0.5, base)

        def finish():
            self.move(base)  # hard snap back
            self._is_shaking = False

        anim.finished.connect(finish)
        anim.start()

        self._shake_anim = anim  # prevent GC