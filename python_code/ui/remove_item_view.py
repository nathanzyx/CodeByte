from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import re

class RemoveItemView(QWidget):  # Changed from QDialog to QWidget
    def __init__(self, parent, inventory_system, patterns):
        super().__init__(parent)
        self.inventory_system = inventory_system
        self.patterns = patterns
        self.setup_ui()
        
    def setup_ui(self):
        # Create a background frame that fills the entire widget
        background_frame = QFrame(self)
        background_frame.setStyleSheet("background-color: #1e1e1e;")
        background_frame.setGeometry(0, 0, self.width(), self.height())
        background_frame.setAutoFillBackground(True)
        
        # Make sure the background frame stays full size when window resizes
        self.resizeEvent = lambda event: background_frame.setGeometry(0, 0, self.width(), self.height())
        
        # Modern color palette with dark theme
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
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Set the background color for the main widget
        self.setStyleSheet(f"background-color: {colors['primary']};")
        
        # Add header section
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)
    
        title = QLabel("Remove Product")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {colors['text_light']};")
        header_layout.addWidget(title)
    
        main_layout.addWidget(header_frame)
        
        # Create a main container with dark background and rounded corners
        main_container = QFrame()
        main_container.setStyleSheet(f"""
            background-color: {colors['container_bg']};
            border-radius: 8px;
            border: none;
        """)
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(20)
        
        # Subtitle
        subtitle = QLabel("Remove items from your inventory")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {colors['placeholder']};")
        container_layout.addWidget(subtitle)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {colors['border']};")
        separator.setFixedHeight(1)
        container_layout.addWidget(separator)
        
        # ID field
        id_container = QFrame()
        id_layout = QVBoxLayout(id_container)
        id_layout.setContentsMargins(0, 10, 0, 10)
        id_layout.setSpacing(8)
        
        id_label = QLabel("Item ID")
        id_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        id_label.setStyleSheet(f"color: {colors['text']};")
        id_layout.addWidget(id_label)
        
        self.id_entry = QLineEdit()
        self.id_entry.setFont(QFont("Segoe UI", 11))
        self.id_entry.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 10px;
                background-color: {colors['input_bg']};
                color: {colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {colors['accent']};
            }}
        """)
        self.id_entry.setPlaceholderText("Enter item ID")
        id_layout.addWidget(self.id_entry)
        
        id_help = QLabel("Enter the ID of the item you want to remove")
        id_help.setFont(QFont("Segoe UI", 9))
        id_help.setStyleSheet(f"color: {colors['placeholder']};")
        id_layout.addWidget(id_help)
        
        container_layout.addWidget(id_container)
        
        # Quantity field
        quantity_container = QFrame()
        quantity_layout = QVBoxLayout(quantity_container)
        quantity_layout.setContentsMargins(0, 10, 0, 10)
        quantity_layout.setSpacing(8)
        
        quantity_label = QLabel("Quantity")
        quantity_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        quantity_label.setStyleSheet(f"color: {colors['text']};")
        quantity_layout.addWidget(quantity_label)
        
        self.count_entry = QLineEdit()
        self.count_entry.setFont(QFont("Segoe UI", 11))
        self.count_entry.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 10px;
                background-color: {colors['input_bg']};
                color: {colors['text']};
            }}
            QLineEdit:focus {{
                border: 1px solid {colors['accent']};
            }}
        """)
        self.count_entry.setPlaceholderText("Enter quantity to remove")
        quantity_layout.addWidget(self.count_entry)
        
        quantity_help = QLabel("Enter the number of items to remove")
        quantity_help.setFont(QFont("Segoe UI", 9))
        quantity_help.setStyleSheet(f"color: {colors['placeholder']};")
        quantity_layout.addWidget(quantity_help)
        
        container_layout.addWidget(quantity_container)
        
        # Warning message with dark theme
        warning_container = QFrame()
        warning_container.setStyleSheet(f"""
            background-color: #422006;
            border-radius: 4px;
        """)
        warning_layout = QHBoxLayout(warning_container)
        warning_layout.setContentsMargins(15, 15, 15, 15)
        warning_layout.setSpacing(10)
        
        warning_icon = QLabel("⚠️")
        warning_icon.setFont(QFont("Segoe UI", 14))
        warning_icon.setStyleSheet("background-color: transparent;")
        warning_layout.addWidget(warning_icon, 0, Qt.AlignmentFlag.AlignTop)
        
        warning_text = QLabel("This action cannot be undone. Please verify the information before proceeding.")
        warning_text.setFont(QFont("Segoe UI", 10))
        warning_text.setWordWrap(True)
        warning_text.setStyleSheet("color: #FBBF24; background-color: transparent;")
        warning_layout.addWidget(warning_text, 1)
        
        container_layout.addWidget(warning_container)
        
        # Add spacer
        container_layout.addStretch()
        
        # Remove button
        remove_btn = QPushButton("Remove Item")
        remove_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['danger']};
                color: white;
                border-radius: 4px;
                padding: 12px 0;
            }}
            QPushButton:hover {{
                background-color: #dc2626;
            }}
        """)
        remove_btn.clicked.connect(self.remove_item)
        container_layout.addWidget(remove_btn)
        
        main_layout.addWidget(main_container)
        
    def remove_item(self):
        # Get values
        item_id = self.id_entry.text().strip()
        item_count = self.count_entry.text().strip()
        
        if not re.match(self.patterns['int'], item_count):
            QMessageBox.critical(self, "Error", "Invalid Count. Please enter a number.")
            return

        if not item_id:
            QMessageBox.critical(self, "Error", "Please enter a valid item ID.")
            return

        try:
            # Try to remove the item from the database
            self.inventory_system.remove_item_from_database(item_id, item_count)
            QMessageBox.information(self, "Success", f"Item with ID {item_id} removed successfully.")
            # Clear the fields after successful removal
            self.id_entry.clear()
            self.count_entry.clear()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    # Add this method to the RemoveItemView class
    def refresh_items(self):
        """Refresh the list of items in the view"""
        # If we have an item list widget, update it
        if hasattr(self, 'item_list'):
            self.item_list.clear()
            
            # Fetch all items from the database
            items = self.inventory_system.get_all_items()
            
            # Add items to the list
            for _, item in items.iterrows():
                item_id = str(item.get('id', ''))
                item_name = str(item.get('name', ''))
                item_text = f"{item_id}: {item_name}"
                self.item_list.addItem(item_text)
        
        # If we have ID dropdown, update it
        if hasattr(self, 'id_combo'):
            self.id_combo.clear()
            items = self.inventory_system.get_all_items()
            for _, item in items.iterrows():
                item_id = str(item.get('id', ''))
                item_name = str(item.get('name', ''))
                self.id_combo.addItem(f"{item_id}: {item_name}", item_id)