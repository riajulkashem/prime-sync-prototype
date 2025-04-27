from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class PaginatedTableWidget(QWidget):
    def __init__(self, columns, data, page_size=100, actions=None):
        super().__init__()
        self.columns = columns
        self.data = data  # List of rows, where each row is a list of values
        self.actions = actions or []
        self.page_size = page_size
        self.current_page = 1
        self.total_pages = (len(self.data) + self.page_size - 1) // self.page_size

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns) + (1 if self.actions else 0))
        headers = self.columns + (["Actions"] if self.actions else [])
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().sectionClicked.connect(self.sort_by_column)

        # Pagination Controls
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.page_label = QLabel(f"Page {self.current_page} of {self.total_pages}")

        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addStretch()

        self.update_table()
        layout.addWidget(self.table)
        layout.addLayout(pagination_layout)

    def update_table(self):
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.data))
        page_data = self.data[start_idx:end_idx]

        self.table.setRowCount(len(page_data))
        for row, item in enumerate(page_data):
            for col, value in enumerate(item[:-1]):  # Exclude actions column data
                table_item = QTableWidgetItem(str(value))
                if col == 2 and "punch" in self.columns[col].lower():  # Highlight punch column
                    table_item.setForeground(Qt.green if value == "IN" else Qt.red)
                elif col == 4 and "status" in self.columns[col].lower():  # Highlight status column
                    table_item.setForeground(Qt.green if value == "Online" else Qt.red)
                self.table.setItem(row, col, table_item)

            if self.actions:
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(0, 0, 0, 0)
                for action_name, icon, callback in self.actions:
                    button = QPushButton()
                    button.setIcon(QIcon(icon))
                    button.setStyleSheet(f"border-radius: 5px; padding: 2px; background-color: {self.get_action_color(action_name)};")
                    button.clicked.connect(lambda checked, r=row, cb=callback: cb(r))
                    actions_layout.addWidget(button)
                self.table.setCellWidget(row, len(self.columns), actions_widget)

        self.page_label.setText(f"Page {self.current_page} of {self.total_pages}")
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)

    def get_action_color(self, action_name):
        colors = {
            "edit": "#4682b4",
            "delete": "#ff4040",
            "connect": "#32cd32",
            "disconnect": "#ff8c00",
            "restart": "#1e90ff"
        }
        return colors.get(action_name.lower(), "#4682b4")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_table()

    def sort_by_column(self, index):
        if index < len(self.columns):
            self.data.sort(key=lambda x: x[index])
            self.current_page = 1
            self.update_table()

    def set_data(self, data, total_pages=None):
        self.data = data
        if total_pages:
            self.total_pages = total_pages
        else:
            self.total_pages = (len(self.data) + self.page_size - 1) // self.page_size
        self.current_page = 1
        self.update_table()