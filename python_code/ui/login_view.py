from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class LoginView(QDialog):
    def __init__(self, parent, logic, inventory_system):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(400, 600)
        # Remove FramelessWindowHint to allow window movement
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setModal(True)
        self.logic = logic
        self.inventory_system = inventory_system
        self.setup_ui()
        
    def setup_ui(self):
        # Modern color palette
        colors = {
            'primary': '#111827',     # Dark background
            'secondary': '#1F2937',   # Slightly lighter dark
            'accent': '#3B82F6',      # Blue accent
            'text': '#F9FAFB',        # Light text
            'text_secondary': '#9CA3AF', # Secondary text
            'border': '#374151',      # Border color
            'input_bg': '#111827',    # Input background
            'error': '#EF4444',       # Error red
        }
        
        # Set window properties
        self.setWindowTitle("Login")
        self.setFixedSize(400, 600)
        # Remove this line
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Remove window frame
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main container with dark background
        main_container = QFrame()
        main_container.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['primary']};
                border-radius: 10px;
                border: 1px solid {colors['border']};
            }}
            QLabel {{
                border: none;
                background-color: transparent;
            }}
        """)
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        
        # Title
        title = QLabel("Welcome Back")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {colors['text']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Please enter your credentials")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {colors['text_secondary']};")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(subtitle)
        
        container_layout.addSpacing(20)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 11))
        username_label.setStyleSheet(f"color: {colors['text']};")
        container_layout.addWidget(username_label)
        
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Enter your username")
        self.username_entry.setFont(QFont("Segoe UI", 11))
        self.username_entry.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 12px;
                min-height: 17px;
                background-color: {colors['input_bg']};
                color: {colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {colors['accent']};
            }}
        """)
        container_layout.addWidget(self.username_entry)
        
        container_layout.addSpacing(10)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11))
        password_label.setStyleSheet(f"color: {colors['text']};")
        container_layout.addWidget(password_label)
        
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Enter your password")
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setFont(QFont("Segoe UI", 11))
        self.password_entry.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 12px;
                min-height: 17px;
                background-color: {colors['input_bg']};
                color: {colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {colors['accent']};
            }}
        """)
        container_layout.addWidget(self.password_entry)
        
        container_layout.addSpacing(30)
        
        # Login button
        login_button = QPushButton("Sign In")
        login_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border-radius: 4px;
                padding: 14px;
                min-height: 16px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #2563EB;
            }}
            QPushButton:pressed {{
                background-color: #1D4ED8;
            }}
        """)
        login_button.clicked.connect(self.authenticate_user)
        container_layout.addWidget(login_button)
        
        # Help text
        help_text = QLabel("Username is 'admin', Password is '321'")
        help_text.setFont(QFont("Segoe UI", 10))
        help_text.setStyleSheet(f"color: {colors['text_secondary']};")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(help_text)
        
        main_layout.addWidget(main_container)

    def authenticate_user(self):
        # Check if the username and password match the hardcoded values
        if self.username_entry.text() == self.inventory_system.username and self.password_entry.text() == self.inventory_system.password:
            self.inventory_system.logged_in = True
            
            QMessageBox.information(self, "Login Successful", "Welcome!")
            # LOG MESSAGE
            self.inventory_system.log_message(f" -- LOGIN SUCCESS: username: {str(self.inventory_system.username)}")
            self.crnt_user = self.username_entry.text()
            
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password")
            # LOG MESSAGE
            self.inventory_system.log_message(f" -- LOGIN FAILED: attempted username: {str(self.username_entry.text())}, attempted password: {str(self.password_entry.text())}")
