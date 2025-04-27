from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PySide6.QtGui import QIcon
from logic.device_logic import DeviceLogic
from ui.components.table_widget import PaginatedTableWidget
from ui.components.form_dialog import FormDialog

class DeviceScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = DeviceLogic(page_size=10)  # Smaller page size for testing
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header_layout = QVBoxLayout()
        title_label = QLabel("Devices")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("Manage connected attendance devices.")
        subtitle_label.setStyleSheet("font-size: 14px; color: gray;")

        header_buttons_layout = QHBoxLayout()
        quick_scan_button = QPushButton("Quick Scan")
        quick_scan_button.setIcon(QIcon("icons/radar.png"))
        quick_scan_button.setStyleSheet("border-radius: 5px; padding: 5px; background-color: green; color: white;")
        quick_scan_button.clicked.connect(lambda: print("Quick Scan clicked"))
        add_device_button = QPushButton("Add Device")
        add_device_button.setIcon(QIcon("icons/plus.png"))
        add_device_button.setStyleSheet("background-color: #4682b4; color: white; border-radius: 5px; padding: 5px;")
        add_device_button.clicked.connect(self.add_device)

        header_buttons_layout.addStretch()
        header_buttons_layout.addWidget(quick_scan_button)
        header_buttons_layout.addWidget(add_device_button)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addLayout(header_buttons_layout)
        layout.addLayout(header_layout)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search devices...")
        self.search_bar.setStyleSheet("border-radius: 10px; padding: 5px;")
        self.search_bar.textChanged.connect(self.filter_devices)
        layout.addWidget(self.search_bar)

        # Table
        devices, _, total_pages = self.logic.get_page()
        self.table_data = [[d.device_model, d.ip_address, d.port, d.password, d.status, d.id] for d in devices]
        actions = [
            ("edit", "icons/pencil.png", self.edit_device),
            ("delete", "icons/bin.png", self.delete_device),
            ("connect", "icons/plug-connect.png", lambda row: print(f"Connect device {self.table_data[row][0]}")),
            ("disconnect", "icons/plug-disconnect.png", lambda row: print(f"Disconnect device {self.table_data[row][0]}")),
            ("restart", "icons/restart.png", lambda row: print(f"Restart device {self.table_data[row][0]}"))
        ]
        self.table = PaginatedTableWidget(["Name", "IP Address", "Port", "Password", "Status"], self.table_data, page_size=10, actions=actions)
        self.table.prev_button.clicked.disconnect()
        self.table.next_button.clicked.disconnect()
        self.table.prev_button.clicked.connect(self.prev_page)
        self.table.next_button.clicked.connect(self.next_page)
        layout.addWidget(self.table)

    def prev_page(self):
        if self.logic.current_page > 1:
            self.logic.load_page(self.logic.current_page - 1)
            self.filter_devices()

    def next_page(self):
        devices, _, total_pages = self.logic.get_page()
        if self.logic.current_page < total_pages:
            self.logic.load_page(self.logic.current_page + 1)
            self.filter_devices()

    def filter_devices(self):
        search_text = self.search_bar.text()
        if search_text:
            filtered_devices, _, total_pages = self.logic.filter_devices(search_text)
        else:
            filtered_devices, _, total_pages = self.logic.get_page()
        self.table_data = [[d.device_model, d.ip_address, d.port, d.password, d.status, d.id] for d in filtered_devices]
        self.table.set_data(self.table_data, total_pages)

    def add_device(self):
        dialog = FormDialog([
            ("Device Model", "text", []),
            ("IP Address", "text", []),
            ("Port", "text", []),
            ("Password", "text", []),
            ("Status", "combo", ["Online", "Offline"])
        ], title="Add Device")
        if dialog.exec():
            self.logic.add_device(dialog.get_data())
            self.filter_devices()

    def edit_device(self, row):
        device_id = self.table_data[row][-1]
        device = next(d for d in self.logic.devices if d.id == device_id)
        dialog = FormDialog([
            ("Device Model", "text", []),
            ("IP Address", "text", []),
            ("Port", "text", []),
            ("Password", "text", []),
            ("Status", "combo", ["Online", "Offline"])
        ], title="Edit Device", data={
            "Device Model": device.device_model,
            "IP Address": device.ip_address,
            "Port": device.port,
            "Password": device.password,
            "Status": device.status
        })
        if dialog.exec():
            self.logic.edit_device(device_id, dialog.get_data())
            self.filter_devices()

    def delete_device(self, row):
        device_id = self.table_data[row][-1]
        self.logic.delete_device(device_id)
        self.filter_devices()