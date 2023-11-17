from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QCheckBox, QLabel, QSpinBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QCheckBox
from PyQt5.QtCore import Qt

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        # ...
        self.setup_ui()


    def setup_ui(self):

        self.max_hours_input = QSpinBox()
        self.max_hours_input.setRange(0, 24)
        self.max_hours_input.setSingleStep(1)
        self.max_hours_input.setValue(8)

        # Create table widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Day", "Weekend"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Add rows to the table
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(day))
            checkbox = QCheckBox()
            self.table.setCellWidget(i, 1, checkbox)
            # center checkbox in cell
            checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")

        # Add OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Add layout to the dialog
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Max hours per day:"))
        layout.addWidget(self.max_hours_input)
        layout.addWidget(QLabel("Track hours for:"))
        layout.addWidget(self.table)
        layout.addWidget(button_box)
        self.setLayout(layout)
