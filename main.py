import sys
import os
import shutil
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QDateEdit, QSpinBox,QFileDialog,
    QTextEdit, QPushButton, QFormLayout, QScrollArea, QMessageBox,
    QDialog, QTableWidget, QTableWidgetItem,QAbstractItemView,QHeaderView,
    QSplitter,
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QAction
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

        # Job details Value holder
        self.job_title_ = 0
        self.record_id = 100

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
        self.right_layout.addWidget(QLabel("Job Title"))
        self.right_layout.addWidget(QLabel(str(self.job_title_)))
        self.right_layout.addWidget(QLabel(str(self.record_id)))

        self.right_layout.addWidget(QLabel("Company"))
        self.right_layout.addWidget(QLabel("Place"))
        self.right_layout.addWidget(QLabel("Type"))

        self.details_label = QLabel("Select a Job to view details")
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.details_label)

        # Right panel content
        self.name_label = QLabel("Contact Person Name")
        self.name_box = QLabel("-")
        self.name_box.setStyleSheet("border: 1px solid gray; padding: 1px; background-color: #f5f5f5; color: black;")

        self.right_layout.addWidget(self.name_label)
        self.right_layout.addWidget(self.name_box)

        # Add panels to splitter 
        self.splitter.addWidget(self.left_panel)
        # splitter.addWidget(self.right_panel)
        self.splitter.setSizes([500, 700])

        # Add splitter to main layout
        self.main_layout.addWidget(self.splitter)

        # Set central widget
        self.setCentralWidget(self.main_widget)

        # Connect click the job event
        self.job_title_ = self.job_table.itemClicked.connect(self.on_row_clicked)

        self.create_menu_bar()
        load_data(self.job_table)

    def on_row_clicked(self, item):
        "Handle when job row is clicked "
        row = item.row()
        self.record_id = self.job_table.item(row,0).text()
        # self.job_title_ = self.job_table.item(row, 1).text()
        email = self.job_table.item(row, 2).text()
        self.pop_detail()
        return self.record_id
    
    def pop_detail(self):
        print ("Hi")
        print(self.record_id)
        self.splitter.addWidget(self.right_panel)
        return 0
   
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
        load_data(self.table)
    
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    window = JobEntryApp()
    window.show()
    sys.exit(app.exec())

        