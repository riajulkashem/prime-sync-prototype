from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

class FormDialog(QDialog):
    def __init__(self, fields, title="Edit Item", data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.fields = fields
        self.data = data or {}
        self.inputs = {}

        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        for field_name, field_type, options in self.fields:
            if field_type == "text":
                input_widget = QLineEdit()
                if field_name.lower() in ["password"]:
                    input_widget.setEchoMode(QLineEdit.Password)
                if field_name in self.data:  # Fixed: Changed self Guns to self.data
                    input_widget.setText(str(self.data[field_name]))
                self.inputs[field_name] = input_widget
            elif field_type == "combo":
                input_widget = QComboBox()
                input_widget.addItems(options)
                if field_name in self.data:
                    input_widget.setCurrentText(str(self.data[field_name]))
                self.inputs[field_name] = input_widget
            layout.addRow(field_name.capitalize(), input_widget)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_data(self):
        return {field: widget.text() if isinstance(widget, QLineEdit) else widget.currentText()
                for field, widget in self.inputs.items()}