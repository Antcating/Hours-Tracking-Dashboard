import sys
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QHeaderView,
)
from PyQt5.QtCore import QTimer, QDate, Qt, QTime
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_date = QDate.currentDate() 
        self.current_day = self.current_date.day()
        self.editing_today_cell = False

        # Set window title and size
        self.setWindowTitle("Hours Tracking Dash")
        self.setGeometry(100, 100, 800, 600)

        # Create timer widget
        self.timer_label = QLabel("0:00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet(
            "font-size: 50px; font-weight: bold; border: 2px solid black; border-radius: 10px;"
        )
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.today_label = QLabel(self.current_date.toString("dddd, MMMM d"))
        self.today_label.setAlignment(Qt.AlignCenter)
        self.today_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; border: 2px solid black; border-radius: 10px;"
        )

        # Create button to show/hide graph
        self.show_graph_button = QPushButton("Show Graph")
        self.show_graph_button.clicked.connect(self.toggle_graph_visibility)

        # Create table widget
        self.table: QTableWidget = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Day of the Month", "Time Worked", "Notes"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.populate_table()
        self.table.cellChanged.connect(self.cell_changed)
        self.table.cellDoubleClicked.connect(self.cell_double_clicked)

        # Create graph widget
        self.graph = plt.figure()
        self.plot_hours_worked()
        self.graph.canvas.hide()

        # Create buttons to start, and add hours to the timer
        self.set_timer_button = QPushButton("Start")
        self.set_timer_button.clicked.connect(self.set_timer)

        # Add widgets to layout
        timer_layout = QHBoxLayout()
        timer_layout.addWidget(self.set_timer_button)
        timer_layout.addWidget(self.timer_label)
        timer_layout.addWidget(self.today_label)
        timer_layout.addWidget(self.show_graph_button)

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)

        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.graph.canvas)

        main_layout = QVBoxLayout()
        main_layout.addLayout(timer_layout)
        main_layout.addLayout(table_layout)
        main_layout.addLayout(graph_layout)

        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def toggle_graph_visibility(self):
        window_ratio = self.width() / self.height()
        if window_ratio > 1.2:
            if self.graph.canvas.isVisible():
                self.graph.canvas.hide()
                self.show_graph_button.setText("Show Graph")
                self.table.show()
            else:
                self.graph.canvas.show()
                self.show_graph_button.setText("Hide Graph")
                self.table.hide()
        else:
            if self.graph.canvas.isVisible():
                self.graph.canvas.hide()
                self.show_graph_button.setText("Hide Graph")
                self.table.show()
            else:
                self.graph.canvas.show()
                self.show_graph_button.setText("Show Graph")
                self.table.show()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event.key() == Qt.Key_T:
            self.set_timer()
        elif event.key() == Qt.Key_R:
            self.reset_selected_cells()
        elif event.key() == Qt.Key_A:
            self.add_hours()
        elif event.key() == Qt.Key_G:
            self.toggle_graph_visibility()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def set_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.set_timer_button.setText("Start")
        else:
            self.timer.start(1000)
            self.set_timer_button.setText("Stop")


    def is_weekend(self, day_of_month):
        date = QDate(self.current_date.year(), self.current_date.month(), day_of_month)
        day_of_week = date.dayOfWeek()
        if day_of_week == Qt.DayOfWeek.Saturday or day_of_week == Qt.DayOfWeek.Sunday:
            return True
        else:
            return False

    def update_timer(self):
        current_time = datetime.datetime.strptime(
            self.timer_label.text(), "%H:%M:%S"
        ).time()
        current_hours = current_time.hour
        current_minutes = current_time.minute
        current_seconds = current_time.second
        total_seconds = (
            current_hours * 3600 + current_minutes * 60 + current_seconds + 1
        )
        new_time = '{:0>8}'.format(str(datetime.timedelta(seconds=total_seconds)))
        # set border of timer to red if over 8 hours
        if current_hours >= 8:
            self.timer_label.setStyleSheet(
                "font-size: 50px; font-weight: bold; border: 2px solid red; border-radius: 10px;"
            )
        else:
            self.timer_label.setStyleSheet(
                "font-size: 50px; font-weight: bold; border: 2px solid green; border-radius: 10px;"
            )
        self.timer_label.setText(new_time)
        # update the time worked for the current day
        if self.editing_today_cell is False:
            time_worked_item = self.table.item(self.current_day - 1, 1)
            time_worked = time_worked_item.text()
            if time_worked:
                time_worked_item.setText(new_time)

    def cell_changed(self, row, column):
        if row == self.table.rowCount() - 1:
            return  # don't allow the total row to be edited

        update_time = self.table.item(row, column)
        new_time = update_time.text()

        if update_time.text() == "":
            new_time = QTime(0, 0, 0).toString("hh:mm:ss")


        elif update_time.text()[-1] == "s":
            new_time = QTime(0, 0, int(update_time.text()[:-1])).toString("hh:mm:ss")

        elif update_time.text()[-1] == "m":
            new_time = QTime(0, int(update_time.text()[:-1]), 0).toString("hh:mm:ss")

        elif update_time.text()[-1] == "h":
            if int(update_time.text()[:-1]) > 24:
                new_time = QTime(24, 0, 0).toString("hh:mm:ss")
            else:
                new_time = QTime(int(update_time.text()[:-1]), 0, 0).toString("hh:mm:ss")

        if new_time != update_time.text():
            update_time.setText(new_time)
            if self.current_date.toString("dd/MM/yyyy") == self.table.item(row, 0).text():
                # if the current day is being edited, update the timer
                self.editing_today_cell = False
                self.timer_label.setText(new_time)

        self.recalculate_total_worked()
        self.plot_hours_worked()

    def cell_double_clicked(self, row, column):
        if self.current_date.toString("dd/MM/yyyy") == self.table.item(row, 0).text():
            self.editing_today_cell = True
        

    def recalculate_total_worked(self):
        total_worked = 0
        for i in range(self.table.rowCount() - 1):
            time_worked = self.table.item(i, 1).text()
            if time_worked:
                qtime_worked = QTime().fromString(time_worked, "hh:mm:ss")
                hours_worked = (
                    qtime_worked.hour()
                    + qtime_worked.minute() / 60
                    + qtime_worked.second() / 3600
                )
                total_worked += hours_worked

        total_worked_formatted = ":".join(
            [
                "{:03d}".format(int(total_worked * 3600 // 3600)),
                "{:02d}".format(int((total_worked * 3600 // 60) % 60)),
                "{:02d}".format(int(total_worked * 3600 % 60)),
            ]
        )
        # set the total worked hours in the last row
        self.table.item(self.table.rowCount() - 1, 1).setText(total_worked_formatted)

    def reset_selected_cells(self):
        selected_cells = self.table.selectedItems()
        for cell in selected_cells:
            cell.setText("00:00:00")
            # Reset the timer if the current day is being reset
            if self.current_date.toString("dd/MM/yyyy") == self.table.item(cell.row(), 0).text():
                self.timer_label.setText("00:00:00")
        self.recalculate_total_worked()
        self.plot_hours_worked()

    def populate_table(self):
        days_in_month = self.current_date.daysInMonth()
        self.table.setRowCount(days_in_month + 1)  # add one row for the total
        total_worked = 0
        for i in range(days_in_month):
            date = QDate(self.current_date.year(), self.current_date.month(), 1).addDays(i)
            self.table.setItem(
                i, 0, QTableWidgetItem(str(QDate.toString(date, "dd/MM/yyyy")))
            )
            self.table.setItem(i, 1, QTableWidgetItem("00:00:00"))
            day_of_month = date.day()
            if self.is_weekend(day_of_month):
                for j in range(self.table.columnCount()):
                    if not self.table.item(i, j):
                        self.table.setItem(i, j, QTableWidgetItem(""))
                    self.table.item(i, j).setBackground(Qt.lightGray)
            # else:
            time_worked = self.table.item(i, 1).text()
            if time_worked:
                qtime_worked = QTime().fromString(time_worked, "hh:mm:ss")
                hours_worked = (
                    qtime_worked.hour()
                    + qtime_worked.minute() / 60
                    + qtime_worked.second() / 3600
                )
                total_worked += hours_worked

        # set the total worked hours in the last row
        self.table.setItem(days_in_month, 0, QTableWidgetItem("Total Worked Hours"))
        self.table.setItem(
            days_in_month,
            1,
            QTableWidgetItem(
                QTime().addSecs(int(total_worked * 3600)).toString("hh:mm:ss")
            ),
        )
        self.table.item(days_in_month, 0).setFlags(Qt.ItemIsEnabled)
        self.table.item(days_in_month, 1).setFlags(Qt.ItemIsEnabled)

    def plot_hours_worked(self):
        worked = []
        for i in range(self.table.rowCount()-1):
            time_worked = self.table.item(i, 1).text()
            if time_worked:
                qtime_worked = QTime().fromString(time_worked, "hh:mm:ss")
                hours_worked = (
                    qtime_worked.hour()
                    + qtime_worked.minute() / 60
                    + qtime_worked.second() / 3600
                )
                worked.append(float(hours_worked))
            else:
                worked.append(0)
        plt.clf()
        sns.set_style("whitegrid")
        sns.barplot(x=range(1, len(worked)+1), y=worked, color="lightblue")
        plt.title("Hours Worked Over the Month")
        plt.xlabel("Days in Current Month")
        plt.ylabel("Hours Worked")
        self.graph.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
