from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout, QLineEdit, QSpinBox, QCheckBox, QLabel, QMessageBox, QTimeEdit
from PySide6.QtCore import Qt, QTime
from logic.settings_logic import SettingsLogic
from utilities.state_manager import state_manager

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = SettingsLogic()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header_layout = QVBoxLayout()
        title_label = QLabel("Settings")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 0;")
        subtitle_label = QLabel("Configure your PrimeSync application settings.")
        subtitle_label.setStyleSheet("font-size: 14px; color: gray; margin-top: -15px; margin-bottom: 15px;")

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addLayout(header_layout)

        # Form for Cloud Connection
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.cloud_api_url = QLineEdit(state_manager.settings["cloud_api_url"])
        self.cloud_api_url.setStyleSheet("border-radius: 5px; padding: 5px;")
        form_layout.addRow("Cloud API URL", self.cloud_api_url)

        self.username = QLineEdit(state_manager.settings["username"])
        self.username.setStyleSheet("border-radius: 5px; padding: 5px;")
        form_layout.addRow("Username", self.username)

        self.password = QLineEdit(state_manager.settings["password"])
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("border-radius: 5px; padding: 5px;")
        form_layout.addRow("Password", self.password)

        self.auto_check_interval = QSpinBox()
        self.auto_check_interval.setRange(1, 60)
        self.auto_check_interval.setValue(state_manager.settings["auto_check_interval"])
        self.auto_check_interval.setStyleSheet("border-radius: 5px; padding: 5px;")
        form_layout.addRow("Auto-Check Interval (minutes)", self.auto_check_interval)

        self.enable_auto_sync = QCheckBox("Enable Auto-Sync")
        self.enable_auto_sync.setChecked(state_manager.settings["enable_auto_sync"])
        form_layout.addRow(self.enable_auto_sync)

        self.periodic_sync_time = QTimeEdit()
        self.periodic_sync_time.setDisplayFormat("h:mm AP")
        time = QTime.fromString(state_manager.settings["periodic_sync_time"], "h:mm AP")
        self.periodic_sync_time.setTime(time)
        self.periodic_sync_time.setStyleSheet("border-radius: 5px; padding: 5px;")
        form_layout.addRow("Periodic Sync", self.periodic_sync_time)

        self.enable_periodic_sync = QCheckBox("Enable Periodic Sync")
        self.enable_periodic_sync.setChecked(state_manager.settings["enable_periodic_sync"])
        form_layout.addRow(self.enable_periodic_sync)

        layout.addLayout(form_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        test_button = QPushButton("Test Connection")
        test_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        test_button.clicked.connect(self.test_connection)

        save_button = QPushButton("Save Settings")
        save_button.setStyleSheet("background-color: #4682b4; color: white; border-radius: 5px; padding: 5px;")
        save_button.clicked.connect(self.save_settings)

        buttons_layout.addWidget(test_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_button)

        layout.addLayout(buttons_layout)

        # Connect to state manager signals
        state_manager.settings_changed.connect(self.on_settings_changed)

    def on_settings_changed(self, settings):
        self.cloud_api_url.setText(settings["cloud_api_url"])
        self.username.setText(settings["username"])
        self.password.setText(settings["password"])
        self.auto_check_interval.setValue(settings["auto_check_interval"])
        self.enable_auto_sync.setChecked(settings["enable_auto_sync"])
        time = QTime.fromString(settings["periodic_sync_time"], "h:mm AP")
        self.periodic_sync_time.setTime(time)
        self.enable_periodic_sync.setChecked(settings["enable_periodic_sync"])

    def test_connection(self):
        if self.logic.test_connection():
            QMessageBox.information(self, "Connection Test", "Connection successful!", QMessageBox.Ok)

    def save_settings(self):
        settings = {
            "cloud_api_url": self.cloud_api_url.text(),
            "username": self.username.text(),
            "password": self.password.text(),
            "auto_check_interval": self.auto_check_interval.value(),
            "enable_auto_sync": self.enable_auto_sync.isChecked(),
            "periodic_sync_time": self.periodic_sync_time.time().toString("h:mm AP"),
            "enable_periodic_sync": self.enable_periodic_sync.isChecked()
        }
        self.logic.save_settings(settings)
        QMessageBox.information(self, "Settings Saved", "Settings saved successfully!", QMessageBox.Ok)