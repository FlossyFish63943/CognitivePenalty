from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QFileDialog,
    QAbstractItemView,
    QInputDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt

from storage import load_blocked_apps, save_blocked_apps


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CognitivePenalty Settings")
        self.setMinimumSize(700, 400)

        central = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Path", "SHA-256"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        button_row = QHBoxLayout()
        add_button = QPushButton("Add App")
        remove_button = QPushButton("Remove Selected")
        refresh_button = QPushButton("Refresh")

        add_button.clicked.connect(self.add_app)
        remove_button.clicked.connect(self.remove_selected)
        refresh_button.clicked.connect(self.refresh)

        button_row.addWidget(add_button)
        button_row.addWidget(remove_button)
        button_row.addStretch()
        button_row.addWidget(refresh_button)

        layout.addWidget(self.table)
        layout.addLayout(button_row)
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.refresh()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def refresh(self):
        apps = load_blocked_apps()
        self.table.setRowCount(0)
        for app in apps:
            self._append_row(app)

    def _append_row(self, app):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(app.get("name", "")))
        self.table.setItem(row, 1, QTableWidgetItem(app.get("path", "")))
        self.table.setItem(row, 2, QTableWidgetItem(app.get("sha256", "")))

    def add_app(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select executable to block",
            str(Path.home()),
            "Executable (*.exe)"
        )
        if not path:
            return

        name, ok = QInputDialog.getText(
            self,
            "Display name",
            "Name for this blocked app:",
            text=Path(path).stem
        )
        if not ok or not name.strip():
            QMessageBox.warning(self, "Missing name", "Please provide a name.")
            return

        apps = load_blocked_apps()
        if any(app.get("path") == path for app in apps):
            QMessageBox.information(
                self,
                "Already blocked",
                "That executable is already in the blocked list."
            )
            return

        apps.append({"name": name.strip(), "path": path})
        save_blocked_apps(apps)
        self.refresh()

    def remove_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Select an app", "Select a row to remove.")
            return

        path_item = self.table.item(row, 1)
        if not path_item:
            return

        path = path_item.text()
        apps = [app for app in load_blocked_apps() if app.get("path") != path]
        save_blocked_apps(apps)
        self.refresh()
