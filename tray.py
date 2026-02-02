from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QObject, Signal


class TrayController(QObject):
    toggle_requested = Signal(bool)
    open_settings_requested = Signal()
    quit_requested = Signal()

    def __init__(self, icon_path=None):
        super().__init__()

        self.tray = QSystemTrayIcon()
        self.tray.setToolTip("CognitivePenalty")

        if icon_path:
            self.tray.setIcon(QIcon(icon_path))

        self.menu = QMenu()

        self.enabled_action = QAction("Enabled")
        self.enabled_action.setCheckable(True)
        self.enabled_action.setChecked(True)
        self.enabled_action.triggered.connect(self.toggle)

        settings_action = QAction("Settings")
        settings_action.triggered.connect(self.open_settings)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.confirm_quit)

        self.menu.addAction(settings_action)
        self.menu.addSeparator()
        self.menu.addAction(self.enabled_action)
        self.menu.addSeparator()
        self.menu.addAction(quit_action)

        self.tray.setContextMenu(self.menu)
        self.tray.show()

    def toggle(self, state):
        self.toggle_requested.emit(state)

    def open_settings(self):
        self.open_settings_requested.emit()

    def confirm_quit(self):
        reply = QMessageBox.question(
            None,
            "Quit CognitivePenalty",
            "Discipline ends here. Quit CognitivePenalty?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.quit_requested.emit()
