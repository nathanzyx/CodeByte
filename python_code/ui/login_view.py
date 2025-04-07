from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QMessageBox, QCheckBox)
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
        
        self.account_exists = self.inventory_system.account_exists()
        
        self.colors = {
            'primary': '#111827',     # Dark background
            'secondary': '#1F2937',   # Slightly lighter dark
            'accent': '#3B82F6',      # Blue accent
            'text': '#F9FAFB',        # Light text
            'text_secondary': '#9CA3AF', # Secondary text
            'border': '#374151',      # Border color
            'input_bg': '#111827',    # Input background
            'error': '#EF4444',       # Error red
        }

        if self.inventory_system.logged_in:
            self.login_credentials_ui()
            return
        if self.account_exists and not self.inventory_system.logged_in:
            self.login_ui()
            return
        if not self.account_exists and not self.inventory_system.logged_in:
            self.setup_login_ui()
            return
    
    #
    #   This function is called with the user is logged in, and allows the user to change credentials an the login requirement
    #
    def login_credentials_ui(self):
        # Set window properties
        self.setWindowTitle("User Profile")
        self.setFixedSize(500, 600)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main container
        main_container = QFrame()
        main_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary']};
                border-radius: 10px;
                border: 1px solid {self.colors['border']};
            }}
            QLabel {{
                border: none;
                background-color: transparent;
            }}
        """)
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        
        title = QLabel(f"{self.inventory_system.username}'s Profile")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['text']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)
        
        subtitle = QLabel("Change Credentials")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {self.colors['text_secondary']};")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(subtitle)
        
        container_layout.addSpacing(20)
        
        # Username fields ---------------------------------
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 11))
        username_label.setStyleSheet(f"color: {self.colors['text']};")
        container_layout.addWidget(username_label)
        
        self.change_username = QLineEdit()
        self.change_username.setPlaceholderText("Username")
        self.change_username.setFont(QFont("Segoe UI", 11))
        self.change_username.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 12px;
                min-height: 17px;
                background-color: {self.colors['input_bg']};
                color: {self.colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
            }}
        """)
        self.change_username.setText(self.inventory_system.username)
        container_layout.addWidget(self.change_username)
        container_layout.addSpacing(5)
            # NEW USERNAME
        # self.new_username = QLineEdit()
        # self.new_username.setPlaceholderText("New username")
        # self.new_username.setFont(QFont("Segoe UI", 11))
        # self.new_username.setStyleSheet(f"""
        #     QLineEdit {{
        #         border: 1px solid {self.colors['border']};
        #         border-radius: 4px;
        #         padding: 12px;
        #         min-height: 17px;
        #         background-color: {self.colors['input_bg']};
        #         color: {self.colors['text']};
        #     }}
        #     QLineEdit:focus {{
        #         border: 1px solid {self.colors['accent']};
        #     }}
        # """)
        # container_layout.addWidget(self.new_username)
        
        # change_username_button = QPushButton("Change Username")
        # change_username_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        # change_username_button.setCursor(Qt.CursorShape.PointingHandCursor)
        # change_username_button.setStyleSheet(f"""
        #     QPushButton {{
        #         background-color: {self.colors['accent']};
        #         color: white;
        #         border-radius: 4px;
        #         padding: 14px;
        #         min-height: 16px;
        #         border: none;
        #     }}
        #     QPushButton:hover {{
        #         background-color: #2563EB;
        #     }}
        #     QPushButton:pressed {{
        #         background-color: #1D4ED8;
        #     }}
        # """)
        # change_username_button.clicked.connect(lambda: self.authenticate_new_credentials(self.old_username.text(), self.change_password.text(), self.new_username.text(), self.new_password.text(), self.require_login_checkbox.isChecked()))
        # container_layout.addWidget(change_username_button)
        
        
        
        container_layout.addSpacing(10)
        
        # Password fields -------------------------------------------------
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11))
        password_label.setStyleSheet(f"color: {self.colors['text']};")
        container_layout.addWidget(password_label)
        
        self.change_password = QLineEdit()
        self.change_password.setPlaceholderText("Password")
        self.change_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.change_password.setFont(QFont("Segoe UI", 11))
        self.change_password.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 12px;
                min-height: 17px;
                background-color: {self.colors['input_bg']};
                color: {self.colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
            }}
        """)
        self.change_password.setText(self.inventory_system.password)
        container_layout.addWidget(self.change_password)
        container_layout.addSpacing(5)
            # NEW PASSWORD
        # self.new_password = QLineEdit()
        # self.new_password.setPlaceholderText("New password")
        # self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        # self.new_password.setFont(QFont("Segoe UI", 11))
        # self.new_password.setStyleSheet(f"""
        #     QLineEdit {{
        #         border: 1px solid {self.colors['border']};
        #         border-radius: 4px;
        #         padding: 12px;
        #         min-height: 17px;
        #         background-color: {self.colors['input_bg']};
        #         color: {self.colors['text']};
        #     }}
        #     QLineEdit:focus {{
        #         border: 1px solid {self.colors['accent']};
        #     }}
        # """)
        # container_layout.addWidget(self.new_password)
        
        
        # Checkbox for "Require Login" checking this will require the user to log in before performing database actions
        self.require_login_checkbox = QCheckBox("Require Login for Database Access")
        self.require_login_checkbox.setFont(QFont("Segoe UI", 11))
        self.require_login_checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
                color: #E5E7EB;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #6B7280;
                background-color: #111827;
            }
            QCheckBox::indicator:checked {
                background-color: #3B82F6;
                border: 1px solid #3B82F6;
            }
        """)
        self.require_login_checkbox.setChecked(True) # True by default
        container_layout.addWidget(self.require_login_checkbox)
        
        
        
        container_layout.addSpacing(30)
        
        # Login button
        login_button = QPushButton("Save Changes")
        login_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent']};
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
        login_button.clicked.connect(lambda: self.authenticate_new_credentials(self.change_username.text(), self.change_password.text(), self.require_login_checkbox.isChecked()))
        container_layout.addWidget(login_button)
        
        main_layout.addWidget(main_container)
    
    
    
    
    
    
    
    #
    #   This function is called if the user has not yet set a username and password (typically if the program is new)
    #
    def setup_login_ui(self):
        self.setWindowTitle("Setup Login")
        self.setFixedSize(500, 600)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main container with dark background
        main_container = QFrame()
        main_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary']};
                border-radius: 10px;
                border: 1px solid {self.colors['border']};
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
        title = QLabel("Setup Login Credentials")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['text']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Please enter your credentials")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {self.colors['text_secondary']};")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(subtitle)
        
        container_layout.addSpacing(20)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 11))
        username_label.setStyleSheet(f"color: {self.colors['text']};")
        container_layout.addWidget(username_label)
        
        self.new_username = QLineEdit()
        self.new_username.setPlaceholderText("Make a username")
        self.new_username.setFont(QFont("Segoe UI", 11))
        self.new_username.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 12px;
                min-height: 17px;
                background-color: {self.colors['input_bg']};
                color: {self.colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
            }}
        """)
        container_layout.addWidget(self.new_username)
        
        container_layout.addSpacing(10)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11))
        password_label.setStyleSheet(f"color: {self.colors['text']};")
        container_layout.addWidget(password_label)
        
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Make a password")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setFont(QFont("Segoe UI", 11))
        self.new_password.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 12px;
                min-height: 17px;
                background-color: {self.colors['input_bg']};
                color: {self.colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
            }}
        """)
        container_layout.addWidget(self.new_password)
        
        
        # Checkbox for Requiring Login
        self.require_login_checkbox = QCheckBox("Require Login")
        self.require_login_checkbox.setFont(QFont("Segoe UI", 11))
        self.require_login_checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
                color: #E5E7EB;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #6B7280;
                background-color: #111827;
            }
            QCheckBox::indicator:checked {
                background-color: #3B82F6;
                border: 1px solid #3B82F6;
            }
        """)
        self.require_login_checkbox.setChecked(True) # We set the default to requiring a login to performing database actions
        container_layout.addWidget(self.require_login_checkbox)
        
        
        
        container_layout.addSpacing(30)
        
        # Login button
        login_button = QPushButton("Set Login Credentials")
        login_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent']};
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
        login_button.clicked.connect(lambda: self.authenticate_new_credentials(self.new_username.text(), self.new_password.text(), self.require_login_checkbox.isChecked()))
        container_layout.addWidget(login_button)
        
        main_layout.addWidget(main_container)
        
    def authenticate_new_credentials(self, change_username, change_password, requires_login):
        if change_username.strip() == "" or change_password.strip() == "":
            QMessageBox.critical(self, "Credentials Not Updated", "A username or password cannot be empty.")
            return
        if " " in change_username or " " in change_password:
            QMessageBox.critical(self, "Credentials Not Updated", "A username or password cannot contain spaces.")
            return
        
        # Check if the username and password match the hardcoded values
        result = self.inventory_system.set_account_credentials(change_username, change_password, requires_login)
        
        if result:
            QMessageBox.information(self, change_username, "Changes Saved!")
            self.crnt_user = change_username
            self.accept()
            
            # Since the user has set their credentials succesfully at this point, we just log them in to save time
            self.inventory_system.login(change_username, change_password)
        else:
            QMessageBox.critical(self, "Credentials Not Updated", "Invalid old username or old password.")

        
    #
    #   This function is called when an account has already been made, and the user has not logged in yet
    #
    def login_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(400, 600)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main container
        main_container = QFrame()
        main_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary']};
                border-radius: 10px;
                border: 1px solid {self.colors['border']};
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
        title.setStyleSheet(f"color: {self.colors['text']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Please enter your credentials")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {self.colors['text_secondary']};")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(subtitle)
        
        container_layout.addSpacing(20)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 11))
        username_label.setStyleSheet(f"color: {self.colors['text']};")
        container_layout.addWidget(username_label)
        
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Enter your username")
        self.username_entry.setFont(QFont("Segoe UI", 11))
        self.username_entry.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 12px;
                min-height: 17px;
                background-color: {self.colors['input_bg']};
                color: {self.colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
            }}
        """)
        container_layout.addWidget(self.username_entry)
        
        container_layout.addSpacing(10)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11))
        password_label.setStyleSheet(f"color: {self.colors['text']};")
        container_layout.addWidget(password_label)
        
        self.change_password = QLineEdit()
        self.change_password.setPlaceholderText("Enter your password")
        self.change_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.change_password.setFont(QFont("Segoe UI", 11))
        self.change_password.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 12px;
                min-height: 17px;
                background-color: {self.colors['input_bg']};
                color: {self.colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
            }}
        """)
        container_layout.addWidget(self.change_password)
        
        container_layout.addSpacing(30)
        
        # Login button
        login_button = QPushButton("Sign In")
        login_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent']};
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

        
        main_layout.addWidget(main_container)

    def authenticate_user(self):
        # Check if the username and password match the hardcoded values
        login_result = self.inventory_system.login(self.username_entry.text(), self.change_password.text())
        
        if login_result:
            QMessageBox.information(self, "Login Successful", "Welcome!")
            self.crnt_user = self.username_entry.text()
            
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password")

