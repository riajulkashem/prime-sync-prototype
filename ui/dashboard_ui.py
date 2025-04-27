from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon
from db.database import Device, User, Attendance
from utilities.device_manager import DeviceManager
from ui.processing_dialog import ProcessingDialog
from ui.error_dialog import ErrorDialog
import requests
from utilities.logger import logger

class DashboardScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header_layout = QVBoxLayout()
        title_label = QLabel("Dashboard")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("Overview of your system.")
        subtitle_label.setStyleSheet("font-size: 14px; color: gray;")

        # Sync buttons
        sync_buttons_layout = QHBoxLayout()
        post_cloud_button = QPushButton("Post Cloud")
        post_cloud_button.setIcon(QIcon("icons/cloud-upload.png"))
        post_cloud_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        post_cloud_button.clicked.connect(self.post_to_cloud)
        pull_device_button = QPushButton("Pull Device")
        pull_device_button.setIcon(QIcon("icons/download.png"))
        pull_device_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        pull_device_button.clicked.connect(self.pull_from_device)

        sync_buttons_layout.addStretch()
        sync_buttons_layout.addWidget(post_cloud_button)
        sync_buttons_layout.addWidget(pull_device_button)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addLayout(sync_buttons_layout)
        layout.addLayout(header_layout)

        # Stats
        stats_layout = QHBoxLayout()
        devices_count = Device.select().count()
        users_count = User.select().count()
        attendance_count = Attendance.select().count()

        devices_card = self.create_stat_card("Devices", str(devices_count), "icons/devices.png")
        users_card = self.create_stat_card("Users", str(users_count), "icons/users.png")
        attendance_card = self.create_stat_card("Attendance Records", str(attendance_count), "icons/attendance.png")

        stats_layout.addWidget(devices_card)
        stats_layout.addWidget(users_card)
        stats_layout.addWidget(attendance_card)
        layout.addLayout(stats_layout)

        layout.addStretch()

    def create_stat_card(self, title, value, icon_path):
        card = QWidget()
        card.setStyleSheet("background-color: #f5f5f5; border-radius: 10px; padding: 15px;")
        card_layout = QHBoxLayout(card)

        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(40, 40))
        card_layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; color: gray;")
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        card_layout.addLayout(text_layout)

        return card

    def post_to_cloud(self):
        """Post all attendance data to the cloud server (abstract implementation)."""
        dialog = ProcessingDialog("Posting to Cloud...")
        dialog.show_with_message("Posting to Cloud...")

        try:
            # Abstract: Simulate posting attendance data to a cloud server
            attendances = Attendance.select().dicts()
            if not attendances:
                dialog.close_after(1000)
                return

            # Simulate API call (replace with actual API endpoint)
            cloud_url = "https://api.primesync.com/v1/attendance"
            response = requests.post(cloud_url, json=list(attendances), timeout=5)
            if response.status_code == 200:
                logger.info(f"Successfully posted {len(attendances)} attendance records to cloud")
                dialog.close_after(2000)  # Simulate processing time
            else:
                logger.error(f"Failed to post to cloud: {response.status_code}")
                dialog.close_after(1000)
                error_dialog = ErrorDialog(f"Failed to post to cloud: HTTP {response.status_code}")
                error_dialog.exec()
        except Exception as e:
            logger.error(f"Error posting to cloud: {e}")
            dialog.close_after(1000)
            error_dialog = ErrorDialog(f"Error posting to cloud: {str(e)}")
            error_dialog.exec()

    def pull_from_device(self):
        """Pull attendance data from all devices."""
        dialog = ProcessingDialog("Pulling from Devices...")
        dialog.show_with_message("Pulling from Devices...")

        try:
            devices = Device.select()
            if not devices:
                logger.info("No devices found to pull attendance from")
                dialog.close_after(1000)
                return

            total_records = 0
            error_messages = []
            for device in devices:
                device_manager = DeviceManager(device)
                success, message = device_manager.pull_attendance()
                if success:
                    if "Pulled" in message:
                        records = int(message.split()[1])
                        total_records += records
                else:
                    error_messages.append(f"Device {device.ip_address}: {message}")

            if error_messages:
                dialog.close_after(1000)
                error_dialog = ErrorDialog("\n".join(error_messages))
                error_dialog.exec()
            else:
                logger.info(f"Total attendance records pulled: {total_records}")
                dialog.close_after(2000)  # Simulate processing time
        except Exception as e:
            logger.error(f"Error pulling attendance from devices: {e}")
            dialog.close_after(1000)
            error_dialog = ErrorDialog(f"Error pulling attendance: {str(e)}")
            error_dialog.exec()