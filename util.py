import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QDateEdit, QSpinBox,QFileDialog,
    QTextEdit, QPushButton, QFormLayout, QScrollArea, QMessageBox,
    QDialog, QTableWidget, QTableWidgetItem,QHeaderView,
)


def connect_db():
    return sqlite3.connect("job_tracker.db")


def load_data(table):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT  title, company, Place, Type, status, salary, date_applied, contact_person, id
        FROM applications
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    table.setRowCount(len(rows))

    for row_idx, row_data in enumerate(rows):
        for col_idx, col_data in enumerate(row_data):
            table.setItem(
                row_idx,
                col_idx,
                QTableWidgetItem(str(col_data) if col_data else "")
            )

    conn.close()


