from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QCheckBox, QLabel, QSpinBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QCheckBox
import json
import os


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
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
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        # Add rows to the table
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(day))
            checkbox = QCheckBox()
            self.table.setCellWidget(i, 1, checkbox)
            # center checkbox in cell
            checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")


        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.reject)

        # Add layout to the dialog
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Max hours per day:"))
        layout.addWidget(self.max_hours_input)
        layout.addWidget(QLabel("Track hours for:"))
        layout.addWidget(self.table)
        layout.addWidget(button_box)
        self.setLayout(layout)

        # Load settings from file or database
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)
            self.max_hours_input.setValue(settings["max_hours"])
            selected_days = settings["weekend_days"]
            for day in selected_days:
                # Set checkbox to checked in the table's row for the day
                checkbox = self.table.cellWidget(day, 1)
                checkbox.setChecked(True)
        else:
            # Create default settings
            settings = {"max_hours": 8, "weekend_days": [5, 6]}
            with open("settings.json", "w") as f:
                json.dump(settings, f)
            for day in settings["weekend_days"]:
                # Set checkbox to checked in the table's row for the day
                checkbox = self.table.cellWidget(day, 1)
                checkbox.setChecked(True)

    def save_settings(self):
        max_hours = self.max_hours_input.value()
        days = 7
        selected_days = []
        for i in range(days):
            checkbox = self.table.cellWidget(i, 1)
            if checkbox.isChecked():
                selected_days.append(i)
        # Save settings to file or database
        settings = {"max_hours": max_hours, "weekend_days": selected_days}
        with open("settings.json", "w") as f:
            json.dump(settings, f)
        self.accept()
