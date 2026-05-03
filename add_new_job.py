import sys
import os
import shutil
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QDateEdit, QSpinBox,QFileDialog,
    QTextEdit, QPushButton, QFormLayout, QScrollArea, QMessageBox,
    QDialog,
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QAction
from util import connect_db, load_data


class NewJobEntry(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Job Tracker")
        self.setMinimumSize(800, 1200)

        # Define where all application data will live
        self.BASE_STORAGE_PATH = os.path.abspath("My_Applications")
        if not os.path.exists(self.BASE_STORAGE_PATH):
            os.makedirs(self.BASE_STORAGE_PATH)                         

        self.init_UI()
        
    
    def init_UI(self):
        #Main Widget
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        self.form_layout = QFormLayout(content_widget)

        #--- INPUT FIELDS ---
        self.title = QLineEdit()
        self.company = QLineEdit()
        self.place = QLineEdit()
        
        self.status = QComboBox()
        self.status.addItems(["Not Applied", "Applied", "In Progress", "Rejected", "Offer"])
        
        self.salary = QSpinBox()
        self.salary.setRange(0, 1000000)
        self.salary.setPrefix("$ ")
        
        self.contact_person = QLineEdit()
        self.contact_email = QLineEdit()
        self.job_ref = QLineEdit()
        
        self.description = QTextEdit()
        
        # Dates (Defaulting to current date)
        self.date_applied = QDateEdit(calendarPopup=True)
        self.date_applied.setDate(QDate.currentDate())
        
        # File Paths (Simple text for now, later we can add browse buttons)
        self.cv_path = QLineEdit()
        self.cover_letter = QLineEdit()

        # Add CV file
        self.cv_path.setReadOnly(True)
        self.cv_path.setPlaceholderText("No file selected")

        # Adding to Form
        self.form_layout.addRow("Job Title*:", self.title)
        self.form_layout.addRow("Company:", self.company)
        self.form_layout.addRow("Location:", self.place)
        self.form_layout.addRow("Status:", self.status)
        self.form_layout.addRow("Salary:", self.salary)
        self.form_layout.addRow("Job Reference:", self.job_ref)
        self.form_layout.addRow("Contact Name:", self.contact_person)
        self.form_layout.addRow("Contact Email:", self.contact_email)
        self.form_layout.addRow("Date Applied:", self.date_applied)
        self.form_layout.addRow("CV File Path:", self.cv_path)
        self.form_layout.addRow("Job Description:", self.description)

         

        # Submit Button
        self.submit_btn = QPushButton("Save Application")
        self.submit_btn.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; padding: 10px;")
        self.submit_btn.clicked.connect(self.save_the_job)

        # Finalizing Layout
        scroll.setWidget(content_widget)
        self.main_layout.addWidget(scroll)
        self.main_layout.addWidget(self.submit_btn)
        self.setCentralWidget(self.main_widget)

        

    

    def create_job_folder(self):
        # Create the specific folder
        folder_name = f"{self.company.text()}_{self.title.text()}_{self.place.text()}"
        target_dir = os.path.join(self.BASE_STORAGE_PATH,folder_name)

        try:
            # Check if the folder exist
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
        except Exception as e :
            QMessageBox.critical(self, "Database Error", f"Error: {str(e)}")

    def save_the_job(self):
        self.create_job_folder()
        self.save_to_db()

    def save_to_db(self):
        # 1. Collect DAta from UI
        data = (
            self.title.text(),
            self.company.text(),
            self.place.text(),
            self.status.currentText(),
            self.salary.value(),
            self.job_ref.text(),
            self.contact_person.text(),
            self.contact_email.text(),
            self.date_applied.date().toString("dd-MM-yyyy"),
            self.description.toPlainText(),
            self.cv_path.text()
        )

        if not self.title.text():
            QMessageBox.warning(self, "Error", "Job Title is required")
            return
                
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO applications 
                (title, company, place, status, salary, job_reference, contact_person, contact_email, date_applied, job_description, cv)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            conn.close()
            reply = QMessageBox.information(self, "Success", "Job saved successfully")
            self.clear_fields()
            
                        
        
        except Exception as e :
            QMessageBox.critical(self, "Database Error", f"Error: {str(e)}")

    def clear_fields(self):
        self.title.clear()
        self.company.clear()
        self.description.clear()



        