from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class ErrorDialog(QDialog):
    def __init__(self, message="An error occurred.", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error")
        self.setFixedSize(300, 150)
        self.setModal(True)
        self.init_ui(message)

    def init_ui(self, message):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Error message
        message_label = QLabel(message)
        message_label.setStyleSheet("font-size: 14px; color: #d32f2f; font-weight: bold;")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        # OK button to close the dialog
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border-radius: 5px;
                padding: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)