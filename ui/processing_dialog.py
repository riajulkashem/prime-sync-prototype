from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer

class ProcessingDialog(QDialog):
    def __init__(self, message="Processing...", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Processing")
        self.setFixedSize(250, 150)
        self.setModal(True)
        self.init_ui(message)

    def init_ui(self, message):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Message label
        message_label = QLabel(message)
        message_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label)

        # Indeterminate progress bar (animated)
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 0)  # Indeterminate mode (continuous animation)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4682b4;
            }
        """)
        layout.addWidget(progress_bar)

    def show_with_message(self, message):
        """Update the message and show the dialog."""
        self.findChild(QLabel).setText(message)
        self.show()

    def close_after(self, duration_ms):
        """Close the dialog after a specified duration."""
        QTimer.singleShot(duration_ms, self.accept)