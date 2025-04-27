from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox
from PySide6.QtGui import QIcon
from logic.user_logic import UserLogic
from ui.components.table_widget import PaginatedTableWidget
from ui.components.form_dialog import FormDialog
from utilities.device_manager import DeviceManager
from ui.processing_dialog import ProcessingDialog
from ui.error_dialog import ErrorDialog
from db.database import Device

class UserScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = UserLogic(page_size=10)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header_layout = QVBoxLayout()
        title_label = QLabel("Users")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("Manage user accounts and permissions.")
        subtitle_label.setStyleSheet("font-size: 14px; color: gray;")

        header_buttons_layout = QHBoxLayout()
        pull_users_button = QPushButton("Pull Users")
        pull_users_button.setIcon(QIcon("icons/download.png"))
        pull_users_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        pull_users_button.clicked.connect(self.pull_users)

        push_users_button = QPushButton("Push Users")
        push_users_button.setIcon(QIcon("icons/upload.png"))
        push_users_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        push_users_button.clicked.connect(self.push_users)

        add_user_button = QPushButton("Add User")
        add_user_button.setIcon(QIcon("icons/user--plus.png"))
        add_user_button.setStyleSheet("background-color: #4682b4; color: white; border-radius: 5px; padding: 5px;")
        add_user_button.clicked.connect(self.add_user)

        header_buttons_layout.addStretch()
        header_buttons_layout.addWidget(pull_users_button)
        header_buttons_layout.addWidget(push_users_button)
        header_buttons_layout.addWidget(add_user_button)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addLayout(header_buttons_layout)
        layout.addLayout(header_layout)

        # Search and Filter
        search_filter_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search users...")
        self.search_bar.setStyleSheet("border-radius: 10px; padding: 5px;")
        self.search_bar.textChanged.connect(self.filter_users)

        self.role_filter = QComboBox()
        self.role_filter.addItems(["All Roles", "Admin", "Manager", "User"])
        self.role_filter.currentTextChanged.connect(self.filter_users)

        import_button = QPushButton()
        import_button.setIcon(QIcon("icons/table-excel.png"))
        import_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        import_button.clicked.connect(self.import_users)

        export_button = QPushButton()
        export_button.setIcon(QIcon("icons/folder-export.png"))
        export_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        export_button.clicked.connect(self.export_users)

        search_filter_layout.addWidget(self.search_bar)
        search_filter_layout.addWidget(self.role_filter)
        search_filter_layout.addWidget(import_button)
        search_filter_layout.addWidget(export_button)
        layout.addLayout(search_filter_layout)

        # Table
        users, _, total_pages = self.logic.get_page()
        self.table_data = [[u.uid, u.name, {1: "Admin", 2: "Manager", 3: "User"}.get(u.role, "Unknown"), str(u.password),
                           str(u.group_id), str(u.user_id), str(u.card), str(u.user_cloud_id), u.uid] for u in users]
        actions = [
            ("edit", "icons/pencil.png", self.edit_user),
            ("delete", "icons/bin--minus.png", self.delete_user)
        ]
        self.table = PaginatedTableWidget(
            ["UID", "Name", "Role", "Password", "Group ID", "User ID", "Card", "Cloud ID"],
            self.table_data,
            page_size=10,
            actions=actions
        )
        self.table.prev_button.clicked.disconnect()
        self.table.next_button.clicked.disconnect()
        self.table.prev_button.clicked.connect(self.prev_page)
        self.table.next_button.clicked.connect(self.next_page)
        layout.addWidget(self.table)

    def prev_page(self):
        if self.logic.current_page > 1:
            self.logic.load_page(self.logic.current_page - 1)
            self.filter_users()

    def next_page(self):
        users, _, total_pages = self.logic.get_page()
        if self.logic.current_page < total_pages:
            self.logic.load_page(self.logic.current_page + 1)
            self.filter_users()

    def filter_users(self):
        search_text = self.search_bar.text()
        role_filter = self.role_filter.currentText()
        if search_text or role_filter != "All Roles":
            filtered_users, _, total_pages = self.logic.filter_users(search_text, role_filter)
        else:
            filtered_users, _, total_pages = self.logic.get_page()
        self.table_data = [[u.uid, u.name, {1: "Admin", 2: "Manager", 3: "User"}.get(u.role, "Unknown"), str(u.password),
                           str(u.group_id), str(u.user_id), str(u.card), str(u.user_cloud_id), u.uid] for u in filtered_users]
        self.table.set_data(self.table_data, total_pages)

    def add_user(self):
        dialog = FormDialog([
            ("Full Name", "text", []),
            ("Role", "combo", ["Admin", "Manager", "User"]),
            ("Password", "text", []),
            ("Group ID", "text", []),
            ("User ID", "text", []),
            ("Card Number", "text", [])
        ], title="Add User")
        if dialog.exec():
            self.logic.add_user(dialog.get_data())
            self.filter_users()
            self.sync_users_to_devices("Adding user to devices...")

    def edit_user(self, row):
        uid = self.table_data[row][-1]
        user = next(u for u in self.logic.users if u.uid == uid)
        dialog = FormDialog([
            ("Full Name", "text", []),
            ("Role", "combo", ["Admin", "Manager", "User"]),
            ("Password", "text", []),
            ("Group ID", "text", []),
            ("User ID", "text", []),
            ("Card Number", "text", [])
        ], title="Edit User", data={
            "Full Name": user.name,
            "Role": {1: "Admin", 2: "Manager", 3: "User"}.get(user.role, "User"),
            "Password": user.password,
            "Group ID": user.group_id,
            "User ID": user.user_id,
            "Card Number": user.card
        })
        if dialog.exec():
            self.logic.edit_user(uid, dialog.get_data())
            self.filter_users()
            self.sync_users_to_devices("Updating user on devices...")

    def delete_user(self, row):
        uid = self.table_data[row][-1]
        self.logic.delete_user(uid)
        self.filter_users()
        self.sync_users_to_devices("Removing user from devices...")

    def import_users(self):
        self.logic.import_users(self)
        self.filter_users()
        self.sync_users_to_devices("Syncing imported users to devices...")

    def export_users(self):
        self.logic.export_users(self)

    def pull_users(self):
        """Pull users from all devices."""
        dialog = ProcessingDialog("Pulling Users from Devices...")
        dialog.show_with_message("Pulling Users from Devices...")

        try:
            devices = Device.select()
            if not devices:
                dialog.close_after(1000)
                error_dialog = ErrorDialog("No devices found to pull users from.")
                error_dialog.exec()
                return

            total_users = 0
            error_messages = []
            for device in devices:
                device_manager = DeviceManager(device)
                success, message = device_manager.pull_users()
                if success:
                    if "Pulled" in message:
                        users = int(message.split()[1])
                        total_users += users
                else:
                    error_messages.append(f"Device {device.ip_address}: {message}")

            if error_messages:
                dialog.close_after(1000)
                error_dialog = ErrorDialog("\n".join(error_messages))
                error_dialog.exec()
            else:
                self.logic.load_page(self.logic.current_page)  # Refresh the user list
                self.filter_users()
                dialog.close_after(2000)
        except Exception as e:
            dialog.close_after(1000)
            error_dialog = ErrorDialog(f"Error pulling users: {str(e)}")
            error_dialog.exec()

    def push_users(self):
        """Push users to all devices."""
        dialog = ProcessingDialog("Pushing Users to Devices...")
        dialog.show_with_message("Pushing Users to Devices...")

        try:
            devices = Device.select()
            if not devices:
                dialog.close_after(1000)
                error_dialog = ErrorDialog("No devices found to push users to.")
                error_dialog.exec()
                return

            total_users = 0
            error_messages = []
            for device in devices:
                device_manager = DeviceManager(device)
                success, message = device_manager.push_users()
                if success:
                    if "Pushed" in message:
                        users = int(message.split()[1])
                        total_users += users
                else:
                    error_messages.append(f"Device {device.ip_address}: {message}")

            if error_messages:
                dialog.close_after(1000)
                error_dialog = ErrorDialog("\n".join(error_messages))
                error_dialog.exec()
            else:
                dialog.close_after(2000)
        except Exception as e:
            dialog.close_after(1000)
            error_dialog = ErrorDialog(f"Error pushing users: {str(e)}")
            error_dialog.exec()

    def sync_users_to_devices(self, message):
        """Sync users to all devices after create/update/delete/import."""
        dialog = ProcessingDialog(message)
        dialog.show_with_message(message)

        try:
            devices = Device.select()
            if not devices:
                dialog.close_after(1000)
                error_dialog = ErrorDialog("No devices found to sync users to.")
                error_dialog.exec()
                return

            total_users = 0
            error_messages = []
            for device in devices:
                device_manager = DeviceManager(device)
                success, message = device_manager.push_users()
                if success:
                    if "Pushed" in message:
                        users = int(message.split()[1])
                        total_users += users
                else:
                    error_messages.append(f"Device {device.ip_address}: {message}")

            if error_messages:
                dialog.close_after(1000)
                error_dialog = ErrorDialog("\n".join(error_messages))
                error_dialog.exec()
            else:
                dialog.close_after(2000)
        except Exception as e:
            dialog.close_after(1000)
            error_dialog = ErrorDialog(f"Error syncing users: {str(e)}")
            error_dialog.exec()