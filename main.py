import sys
import os
import shutil
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QSpinBox,
    QFileDialog, QTextEdit, QPushButton, QFormLayout, QScrollArea,
    QMessageBox, QDialog, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView, QSplitter,
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QAction, QFont
from add_new_job import NewJobEntry
from util import load_data


class JobEntryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Job Tracker")
        self.setGeometry(100,100,1000,600)
        self.init_UI()

        
    
    def init_UI(self):
        #Main Widget
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # create splitter
        self.splitter = QSplitter()

        #  Left Panel
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.addWidget(QLabel("Job Vacancies"))
        
        # List of Jobs as Table in left panel
        self.job_table = QTableWidget()
        self.job_table.setColumnCount(7)
        self.job_table.setHorizontalHeaderLabels(["Title", "Company", "Place", "Type", "Status", "Salary", "Date Applied" ])
        self.job_table.resizeColumnsToContents()
        self.job_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.job_table.setEditTriggers(self.job_table.EditTrigger.NoEditTriggers)
        # Justify the Table
        header = self.job_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Title
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Company
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # Place
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # Type
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Salary
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents) # Date

        # Add table to layout
        self.left_layout.addWidget(self.job_table)

        # Right Panel
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(12, 12, 12, 12)
        self.right_layout.setSpacing(8)

        header = QLabel("Job Details")
        header_font = QFont()
        header_font.setPointSize(13)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(header)

        self.details_label = QLabel("Select a job to view details")
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.details_label.setStyleSheet("color: gray; font-style: italic;")
        self.right_layout.addWidget(self.details_label)

        # Grid for the 7 job fields
        self._field_names = ["Title", "Company", "Place", "Type", "Status", "Salary", "Date Applied"]
        self._field_values = []

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)

        label_style = "font-weight: bold;"
        value_style = "border: 1px solid #ccc; padding: 4px; background-color: #f9f9f9; border-radius: 3px;"

        for row, name in enumerate(self._field_names):
            lbl = QLabel(name + ":")
            lbl.setStyleSheet(label_style)
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            val = QLabel("-")
            val.setStyleSheet(value_style)
            val.setWordWrap(True)

            grid.addWidget(lbl, row, 0)
            grid.addWidget(val, row, 1)
            self._field_values.append(val)

        self.right_layout.addWidget(grid_widget)
        self.right_layout.addStretch()

        # Add both panels to splitter
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([500, 500])

        # Add splitter to main layout
        self.main_layout.addWidget(self.splitter)

        # Set central widget
        self.setCentralWidget(self.main_widget)

        self.job_table.cellClicked.connect(self.on_row_clicked)

        self.create_menu_bar()
        load_data(self.job_table)

    def on_row_clicked(self, row, col):
        self.details_label.hide()
        for c, val_label in enumerate(self._field_values):
            cell = self.job_table.item(row, c)
            val_label.setText(cell.text() if cell and cell.text() else "-")
   
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        new_action = QAction("New",self)
        save_action = QAction("Save", self)
        refresh_action = QAction("Refresh",self)
        setting_action = QAction("Setting", self)
        close_action = QAction("Close", self)

        edit_menu = menu_bar.addMenu("Edit")
        help_menu = menu_bar.addMenu("Help")
        new_action.triggered.connect(self.on_new)
        refresh_action.triggered.connect(self.on_refresh)
        close_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(refresh_action)
        file_menu.addAction(save_action)
        file_menu.addAction(setting_action)
        file_menu.addAction(close_action)

    def on_new(self):
        self.dialog = NewJobEntry()
        self.dialog.show()
        # if result == QDialog.DialogCode.Accepted:
        #     print("New job successfully created.")
        # else:
        #     print("New job canceled.")
    
    def on_refresh(self):
        load_data(self.job_table)
    
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    window = JobEntryApp()
    window.show()
    sys.exit(app.exec())

        