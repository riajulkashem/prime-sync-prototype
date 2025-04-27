from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QDateEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
from logic.attendance_logic import AttendanceLogic
from ui.components.table_widget import PaginatedTableWidget

class AttendanceScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = AttendanceLogic(page_size=10)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header_layout = QVBoxLayout()
        title_label = QLabel("Attendance")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("View and manage attendance records.")
        subtitle_label.setStyleSheet("font-size: 14px; color: gray;")

        header_buttons_layout = QHBoxLayout()
        pull_attendance_button = QPushButton("Pull Attendance")
        pull_attendance_button.setIcon(QIcon("icons/download.png"))
        pull_attendance_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        pull_attendance_button.clicked.connect(lambda: print("Pull Attendance clicked"))

        export_button = QPushButton("Export")
        export_button.setIcon(QIcon("icons/folder-export.png"))
        export_button.setStyleSheet("border-radius: 5px; padding: 5px;")
        export_button.clicked.connect(self.export_attendance)

        header_buttons_layout.addStretch()
        header_buttons_layout.addWidget(pull_attendance_button)
        header_buttons_layout.addWidget(export_button)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addLayout(header_buttons_layout)
        layout.addLayout(header_layout)

        # Search and Filter
        search_filter_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search attendance...")
        self.search_bar.setStyleSheet("border-radius: 10px; padding: 5px;")
        self.search_bar.textChanged.connect(self.filter_attendance)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.start_date.setStyleSheet("border-radius: 5px; padding: 5px;")
        self.start_date.dateChanged.connect(self.filter_attendance)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet("border-radius: 5px; padding: 5px;")
        self.end_date.dateChanged.connect(self.filter_attendance)

        search_filter_layout.addWidget(self.search_bar)
        search_filter_layout.addWidget(QLabel("From:"))
        search_filter_layout.addWidget(self.start_date)
        search_filter_layout.addWidget(QLabel("To:"))
        search_filter_layout.addWidget(self.end_date)
        layout.addLayout(search_filter_layout)

        # Table
        attendances, _, total_pages = self.logic.get_page()
        self.table_data = [[a.id, a.timestamp, a.user, a.status, a.punch, a.uid] for a in attendances]
        self.table = PaginatedTableWidget(
            ["ID", "Timestamp", "User", "Status", "Punch", "UID"],
            self.table_data,
            page_size=10
        )
        self.table.prev_button.clicked.disconnect()
        self.table.next_button.clicked.disconnect()
        self.table.prev_button.clicked.connect(self.prev_page)
        self.table.next_button.clicked.connect(self.next_page)
        layout.addWidget(self.table)

    def prev_page(self):
        if self.logic.current_page > 1:
            self.logic.load_page(self.logic.current_page - 1)
            self.filter_attendance()

    def next_page(self):
        attendances, _, total_pages = self.logic.get_page()
        if self.logic.current_page < total_pages:
            self.logic.load_page(self.logic.current_page + 1)
            self.filter_attendance()

    def filter_attendance(self):
        search_text = self.search_bar.text()
        start_date = self.start_date.date().toPython()
        end_date = self.end_date.date().toPython().replace(hour=23, minute=59, second=59)
        date_filter = (start_date, end_date) if start_date and end_date else None

        if search_text or date_filter:
            filtered_attendances, _, total_pages = self.logic.filter_attendance(search_text, date_filter)
        else:
            filtered_attendances, _, total_pages = self.logic.get_page()

        self.table_data = [[a.id, a.timestamp, a.user, a.status, a.punch, a.uid] for a in filtered_attendances]
        self.table.set_data(self.table_data, total_pages)

    def export_attendance(self):
        self.logic.export_attendance(self)