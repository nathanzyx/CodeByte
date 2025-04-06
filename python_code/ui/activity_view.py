from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import re

class ActivityView(QWidget):
    def __init__(self, root, logic, inventory_system):
        super().__init__()
        self.root = root
        self.logic = logic
        self.inventory_system = inventory_system

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Set up a timer to refresh the file contents
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.load_file_contents)
        self.refresh_timer.start(1000)

        self.setup_ui()
        
        

    def setup_ui(self):
        colors = {
            'primary': '#111827',     # Dark background
            'container_bg': '#1F2937', # Dark container background
            'input_bg': '#111827',    # Dark input background
            'text': '#E5E7EB',        # Light text for dark background
            'text_light': '#F9FAFB',  # Light text for dark backgrounds
            'accent': '#3B82F6',      # Blue accent
            'danger': '#ef4444',      # Error/danger red
            'warning': '#f59e0b',     # Warning orange
            'border': '#374151',      # Dark border
            'placeholder': '#9ca3af', # Placeholder text
        }

        # Set the background color for the main widget
        self.setStyleSheet(f"background-color: {colors['primary']};")

        # Add header section
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)

        title = QLabel("Activity")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {colors['text_light']};")
        header_layout.addWidget(title)

        self.main_layout.addWidget(header_frame)

        # Main container
        main_container = QFrame()
        main_container.setStyleSheet(f"""
            background-color: {colors['container_bg']};
            border-radius: 8px;
            border: none;
        """)
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(20)

        # QTextEdit to display file contents
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        
        self.text_display.setStyleSheet(f"""
            background-color: {colors['input_bg']};
            color: {colors['text']};
            border: none;
            padding: 10px;
        """)
        self.text_display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_display.setFont(QFont("Segoe UI", 12))
        container_layout.addWidget(self.text_display)

        self.main_layout.addWidget(main_container)

        # Load and display filee contents
        self.load_file_contents()
        self.text_display.moveCursor(self.text_display.textCursor().MoveOperation.End)
        
        
    def load_file_contents(self):
        try:
            file_name = f"{self.inventory_system.name}.txt"
            with open(file_name, "r") as file:
                contents = file.read()

            current_contents = self.text_display.toPlainText()

            # Only update if content changed
            if current_contents != contents:
                # Save scroll position
                vertical_scrollbar = self.text_display.verticalScrollBar()
                current_scroll_pos = vertical_scrollbar.value()

                self.text_display.setPlainText(contents)

                # Restore scroll position
                vertical_scrollbar.setValue(current_scroll_pos)

        except FileNotFoundError:
            self.text_display.setPlainText("No activity log found.")
        except Exception as e:
            self.text_display.setPlainText(f"Error loading activity log: {str(e)}")