import sys
from db.database import init_db, Device, User, Attendance

from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from ui.device_ui import DeviceScreen
from ui.user_ui import UserScreen
from ui.attendance_ui import AttendanceScreen
from ui.settings_ui import SettingsScreen
from ui.dashboard_ui import DashboardScreen
from ui.developer_credits import DeveloperCreditsDialog  # Import the new dialog
import datetime
from utilities.logger import logger

class PrimeSyncApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrimeSync")
        self.setGeometry(100, 100, 1200, 700)

        # Add sample data
        self.init_db_with_sample_data()

        # Set up the main UI
        self.init_ui()

    def init_db_with_sample_data(self):
        if not Device.select().exists():
            device = Device.create(
                ip_address="192.168.1.100",
                port=4370,
                password="1234",
                device_model="Device 1",
                status="Online"
            )
            logger.info("Added sample device")
        else:
            device = Device.select().first()

        if not User.select().exists():
            user = User.create(
                uid=1,
                name="John Doe",
                role=1,  # Admin
                password="password123",
                group_id=1,
                user_id="U001",
                card="CARD001",
                user_cloud_id=1001,
                device=device
            )
            logger.info("Added sample user")
        else:
            user = User.select().first()

        if not Attendance.select().exists():
            Attendance.create(
                user=user,
                timestamp=datetime.datetime.now(),
                status="Check-In",
                punch="IN",
                uid=user.uid
            )
            logger.info("Added sample attendance record")

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Sidebar
        sidebar_widget = self.create_sidebar()
        main_layout.addWidget(sidebar_widget, 1)

        # Content area
        self.stacked_widget = QStackedWidget()
        self.screen_classes = [
            DashboardScreen,
            DeviceScreen,
            UserScreen,
            AttendanceScreen,
            SettingsScreen
        ]
        self.screens = [None] * len(self.screen_classes)
        self.screens[0] = DashboardScreen(self)
        self.stacked_widget.addWidget(self.screens[0])
        for _ in range(len(self.screen_classes) - 1):
            self.stacked_widget.addWidget(QWidget())
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(content_widget, 4)

    def create_sidebar(self):
        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("background-color: #483d8b;")
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setAlignment(Qt.AlignTop)

        # Sidebar title
        sidebar_title = QLabel("PrimeSync")
        sidebar_title.setStyleSheet("font-size: 20px; font-weight: bold; color: white; margin: 20px;")
        sidebar_layout.addWidget(sidebar_title)

        # Sidebar buttons
        self.buttons = []
        menu_items = [
            ("Dashboard", "icons/dashboard.png", 0),
            ("Devices", "icons/devices.png", 1),
            ("Users", "icons/users.png", 2),
            ("Attendance", "icons/attendance.png", 3),
            ("Settings", "icons/settings.png", 4),
        ]

        for name, icon_path, index in menu_items:
            button = QPushButton(name)
            button.setIcon(QIcon(icon_path))
            button.setStyleSheet("background-color: transparent; color: white; border: none; padding: 10px; margin: 5px; text-align: left;")
            button.clicked.connect(lambda checked, idx=index, btn=button, n=name: self.switch_screen(idx, btn, n))
            sidebar_layout.addWidget(button)
            self.buttons.append(button)

        # Set Dashboard as the default active button
        self.active_button = self.buttons[0]
        self.active_button.setStyleSheet("background-color: #6a5acd; color: white; border-radius: 5px; padding: 10px; margin: 5px; text-align: left;")

        # Spacer and bottom buttons
        sidebar_layout.addStretch()
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        # Quit button
        quit_button = QPushButton("Quit")
        quit_button.setStyleSheet("background-color: transparent; color: white; border: 1px solid white; border-radius: 5px; padding: 5px;")
        quit_button.clicked.connect(self.quit_application)
        bottom_layout.addWidget(quit_button)

        # Developer button
        help_button = QPushButton("Developer")
        help_button.setStyleSheet("background-color: transparent; color: white; border: 1px solid white; border-radius: 5px; padding: 5px;")
        help_button.clicked.connect(self.show_developer_credits)
        bottom_layout.addWidget(help_button)

        sidebar_layout.addWidget(bottom_widget)

        return sidebar_widget

    def switch_screen(self, index, button, screen_name):
        logger.info(f"{screen_name} clicked")
        if self.screens[index] is None:
            logger.info(f"Initializing {screen_name} screen")
            self.screens[index] = self.screen_classes[index]()
            self.stacked_widget.removeWidget(self.stacked_widget.widget(index))
            self.stacked_widget.insertWidget(index, self.screens[index])
        self.stacked_widget.setCurrentIndex(index)
        if self.active_button:
            self.active_button.setStyleSheet("background-color: transparent; color: white; border: none; padding: 10px; margin: 5px; text-align: left;")
        button.setStyleSheet("background-color: #6a5acd; color: white; border-radius: 5px; padding: 10px; margin: 5px; text-align: left;")
        self.active_button = button

    def quit_application(self):
        logger.info("Quit button clicked, closing application")
        QApplication.quit()

    def show_developer_credits(self):
        dialog = DeveloperCreditsDialog(self)
        dialog.exec()

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = PrimeSyncApp()
    window.show()
    sys.exit(app.exec())