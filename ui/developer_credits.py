from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon, QPainter, QPainterPath
import webbrowser


class DeveloperCreditsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Developer Credits")
        self.setFixedSize(300, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(10, 10, 10, 10)

        layout.addLayout(self.create_profile_image("riajulkashem.png", 120))
        layout.addWidget(self.create_label("Riajul Kashem", 18, bold=True))
        layout.addWidget(self.create_label("Software Engineer & Full-Stack Developer", 12, gray=True, wrap=True))
        layout.addLayout(self.create_social_buttons())

        description_text = "Riajul Kashem is a software engineer and web developer, specializing in Python, Django, and web automation. He offers services such as web scraping, data extraction, and full-stack web application development."
        description_label = self.create_label(description_text, 11, wrap=True)
        description_label.setStyleSheet("color: #555;")  # Slightly lighter color for description
        layout.addWidget(description_label)
        layout.addStretch()


    def create_profile_image(self, image_path, size):
        profile_label = QLabel()
        profile_label.setFixedSize(size, size)
        profile_label.setStyleSheet(f"""
            border: 2px solid #d0d0d0;
            border-radius: {size // 2}px;
        """)

        pixmap = self.create_circular_pixmap(image_path, size)
        profile_label.setPixmap(pixmap)

        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addWidget(profile_label)
        wrapper.addStretch()
        return wrapper

    def create_circular_pixmap(self, path, size):
        original = QPixmap(path)
        if original.isNull():
            fallback = QPixmap(size, size)
            fallback.fill(Qt.transparent)
            painter = QPainter(fallback)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.setClipPath(path)
            painter.fillPath(path, Qt.lightGray)
            painter.end()
            return fallback

        original = original.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        final = QPixmap(size, size)
        final.fill(Qt.transparent)

        painter = QPainter(final)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        x = (size - original.width()) // 2
        y = (size - original.height()) // 2
        painter.drawPixmap(x, y, original)
        painter.end()

        return final

    def create_label(self, text, size, bold=False, gray=False, wrap=False):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(wrap)
        color = "gray" if gray else "#333"
        weight = "bold" if bold else "normal"
        label.setStyleSheet(f"font-size: {size}px; font-weight: {weight}; color: {color};")
        return label

    def create_social_buttons(self):
        social_links = [
            ("icons/github.png", "https://github.com/riajulkashem"),
            ("icons/linkedin.png", "https://linkedin.com/in/riajulkashem"),
            ("icons/facebook.png", "https://facebook.com/riajul.kashem"),
            ("icons/x.png", "https://x.com/riajulkashem"),
        ]

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        for icon_path, url in social_links:
            btn = QPushButton()
            icon_size = 24
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(icon_size, icon_size))
            btn.setFixedSize(icon_size, icon_size)  # Exactly icon size
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    padding: 0px;
                    margin: 0px;
                    background: transparent;
                }
            """)
            btn.clicked.connect(lambda _, link=url: webbrowser.open(link))
            layout.addWidget(btn)

        return layout
