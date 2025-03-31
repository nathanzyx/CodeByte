from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QFrame, QMessageBox, QScrollArea,
                            QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ManageFieldsView(QWidget):  # Changed from QDialog to QWidget
    def __init__(self, parent, logic, inventory_system):
        super().__init__(parent)
        self.logic = logic
        self.inventory_system = inventory_system
        # Define colors as an instance attribute so it's accessible in all methods
        self.colors = {
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
        self.setup_ui()

    def setup_ui(self):
        # Create a background frame that fills the entire widget
        background_frame = QFrame(self)
        background_frame.setStyleSheet("background-color: #1e1e1e;")
        background_frame.setGeometry(0, 0, self.width(), self.height())
        background_frame.setAutoFillBackground(True)
        
        # Make sure the background frame stays full size when window resizes
        self.resizeEvent = lambda event: background_frame.setGeometry(0, 0, self.width(), self.height())
        
        # Use self.colors instead of local colors variable
        colors = self.colors
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Set the background color for the main widget
        self.setStyleSheet(f"background-color: {colors['primary']};")
        
        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)

        title = QLabel("Database Fields Management")
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
        
        # Tab buttons
        tab_frame = QFrame()
        tab_frame.setStyleSheet(f"background-color: transparent;")
        tab_buttons_layout = QHBoxLayout(tab_frame)
        tab_buttons_layout.setContentsMargins(0, 0, 0, 20)
        tab_buttons_layout.setSpacing(10)
        
        # Create stacked widget for tab content
        self.tab_stack = QStackedWidget()
        
        # Tab buttons
        self.add_btn = QPushButton("Add Field")
        self.add_btn.setFont(QFont("Segoe UI", 11))
        self.add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border-radius: 4px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: #2563EB;
            }}
        """)
        self.add_btn.clicked.connect(lambda: self.show_tab(0))
        
        self.remove_btn = QPushButton("Remove Field")
        self.remove_btn.setFont(QFont("Segoe UI", 11))
        self.remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['border']};
                color: {colors['text']};
                border-radius: 4px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: #4B5563;
            }}
        """)
        self.remove_btn.clicked.connect(lambda: self.show_tab(1))
        
        tab_buttons_layout.addWidget(self.add_btn)
        tab_buttons_layout.addWidget(self.remove_btn)
        tab_buttons_layout.addStretch()
        
        container_layout.addWidget(tab_frame)
        
        # Create tab pages
        add_tab = QWidget()
        add_tab.setStyleSheet(f"background-color: transparent;")
        add_layout = QVBoxLayout(add_tab)
        add_layout.setContentsMargins(0, 0, 0, 0)
        add_layout.setSpacing(15)
        
        remove_tab = QWidget()
        remove_tab.setStyleSheet(f"background-color: transparent;")
        remove_layout = QVBoxLayout(remove_tab)
        remove_layout.setContentsMargins(0, 0, 0, 0)
        remove_layout.setSpacing(15)
        
        # Add tabs to stack
        self.tab_stack.addWidget(add_tab)
        self.tab_stack.addWidget(remove_tab)
        
        container_layout.addWidget(self.tab_stack)
        
        # Add Field Tab Content
        add_title = QLabel("Field Management")
        add_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        add_title.setStyleSheet(f"color: {colors['text']};")
        add_layout.addWidget(add_title)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {colors['border']};")
        separator.setFixedHeight(1)
        add_layout.addWidget(separator)
        
        # Field name input
        field_name_container = QFrame()
        field_name_layout = QVBoxLayout(field_name_container)
        field_name_layout.setContentsMargins(0, 10, 0, 10)
        field_name_layout.setSpacing(8)
        
        field_name_label = QLabel("Field Name")
        field_name_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        field_name_label.setStyleSheet(f"color: {colors['text']};")
        field_name_layout.addWidget(field_name_label)
        
        self.field_name_entry = QLineEdit()
        self.field_name_entry.setFont(QFont("Segoe UI", 11))
        self.field_name_entry.setStyleSheet(f"""
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
        self.field_name_entry.setPlaceholderText("Enter field name")
        field_name_layout.addWidget(self.field_name_entry)
        
        field_name_help = QLabel("Enter a unique name for the new field")
        field_name_help.setFont(QFont("Segoe UI", 9))
        field_name_help.setStyleSheet(f"color: {colors['placeholder']};")
        field_name_layout.addWidget(field_name_help)
        
        add_layout.addWidget(field_name_container)
        
        # Set default entry type since we removed the selection UI
        self.entry_type = "text_box_s"
        
        # Validation Type Selection
        validation_type_container = QFrame()
        validation_type_layout = QVBoxLayout(validation_type_container)
        validation_type_layout.setContentsMargins(0, 10, 0, 10)
        validation_type_layout.setSpacing(8)
        
        validation_type_label = QLabel("Validation Type")
        validation_type_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        validation_type_label.setStyleSheet(f"color: {colors['text']};")
        validation_type_layout.addWidget(validation_type_label)
        
        validation_type_buttons = QFrame()
        validation_type_buttons_layout = QHBoxLayout(validation_type_buttons)
        validation_type_buttons_layout.setContentsMargins(0, 0, 0, 0)
        validation_type_buttons_layout.setSpacing(10)
        
        self.validation_type = "string"
        self.validation_buttons = []
        
        string_btn = QPushButton("String")
        string_btn.setFont(QFont("Segoe UI", 11))
        string_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border-radius: 4px;
                padding: 10px 15px;
            }}
            QPushButton:hover {{
                background-color: #2563EB;
            }}
        """)
        string_btn.clicked.connect(lambda: self.set_validation_type("string"))
        self.validation_buttons.append(string_btn)
        
        int_btn = QPushButton("Integer")
        int_btn.setFont(QFont("Segoe UI", 11))
        int_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['border']};
                color: {colors['text']};
                border-radius: 4px;
                padding: 10px 15px;
            }}
            QPushButton:hover {{
                background-color: #4B5563;
            }}
        """)
        int_btn.clicked.connect(lambda: self.set_validation_type("int"))
        self.validation_buttons.append(int_btn)
        
        float_btn = QPushButton("Decimal")
        float_btn.setFont(QFont("Segoe UI", 11))
        float_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['border']};
                color: {colors['text']};
                border-radius: 4px;
                padding: 10px 15px;
            }}
            QPushButton:hover {{
                background-color: #4B5563;
            }}
        """)
        float_btn.clicked.connect(lambda: self.set_validation_type("float"))
        self.validation_buttons.append(float_btn)
        validation_type_buttons_layout.addWidget(string_btn)
        validation_type_buttons_layout.addWidget(int_btn)
        validation_type_buttons_layout.addWidget(float_btn)
        validation_type_buttons_layout.addStretch()
        
        validation_type_layout.addWidget(validation_type_buttons)
        
        validation_type_help = QLabel("Select the validation type for the field")
        validation_type_help.setFont(QFont("Segoe UI", 9))
        validation_type_help.setStyleSheet(f"color: {colors['placeholder']};")
        validation_type_layout.addWidget(validation_type_help)
        
        add_layout.addWidget(validation_type_container)
        
        # Required Selection
        required_container = QFrame()
        required_layout = QVBoxLayout(required_container)
        required_layout.setContentsMargins(0, 10, 0, 10)
        required_layout.setSpacing(8)
        
        required_label = QLabel("Required Field")
        required_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        required_label.setStyleSheet(f"color: {colors['text']};")
        required_layout.addWidget(required_label)
        
        required_buttons = QFrame()
        required_buttons_layout = QHBoxLayout(required_buttons)
        required_buttons_layout.setContentsMargins(0, 0, 0, 0)
        required_buttons_layout.setSpacing(10)
        
        self.required = "1"
        self.required_buttons = []
        
        yes_btn = QPushButton("Yes")
        yes_btn.setFont(QFont("Segoe UI", 11))
        yes_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border-radius: 4px;
                padding: 10px 15px;
            }}
            QPushButton:hover {{
                background-color: #2563EB;
            }}
        """)
        yes_btn.clicked.connect(lambda: self.set_required("1"))
        self.required_buttons.append(yes_btn)
        
        no_btn = QPushButton("No")
        no_btn.setFont(QFont("Segoe UI", 11))
        no_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['border']};
                color: {colors['text']};
                border-radius: 4px;
                padding: 10px 15px;
            }}
            QPushButton:hover {{
                background-color: #4B5563;
            }}
        """)
        no_btn.clicked.connect(lambda: self.set_required("0"))
        self.required_buttons.append(no_btn)
        required_buttons_layout.addWidget(yes_btn)
        required_buttons_layout.addWidget(no_btn)
        required_buttons_layout.addStretch()
        
        required_layout.addWidget(required_buttons)
        
        required_help = QLabel("Specify if this field is required")
        required_help.setFont(QFont("Segoe UI", 9))
        required_help.setStyleSheet(f"color: {colors['placeholder']};")
        required_layout.addWidget(required_help)
        
        add_layout.addWidget(required_container)
        
        # Add spacer
        add_layout.addStretch()
        
        # Add button
        add_field_btn = QPushButton("Add Field")
        add_field_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        add_field_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border-radius: 4px;
                padding: 12px 0;
            }}
            QPushButton:hover {{
                background-color: #2563EB;
            }}
        """)
        add_field_btn.clicked.connect(self.add_field)
        add_layout.addWidget(add_field_btn)
        
        # Remove Field Tab Content
        remove_title = QLabel("Remove Field")
        remove_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        remove_title.setStyleSheet(f"color: {colors['text']};")
        remove_layout.addWidget(remove_title)
        
        # Separator for remove tab
        remove_separator = QFrame()
        remove_separator.setFrameShape(QFrame.Shape.HLine)
        remove_separator.setStyleSheet(f"background-color: {colors['border']};")
        remove_separator.setFixedHeight(1)
        remove_layout.addWidget(remove_separator)
        
        # Field name input for removal
        remove_field_container = QFrame()
        remove_field_layout = QVBoxLayout(remove_field_container)
        remove_field_layout.setContentsMargins(0, 10, 0, 10)
        remove_field_layout.setSpacing(8)
        
        remove_field_label = QLabel("Field Name")
        remove_field_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        remove_field_label.setStyleSheet(f"color: {colors['text']};")
        remove_field_layout.addWidget(remove_field_label)
        
        self.remove_field_entry = QLineEdit()
        self.remove_field_entry.setFont(QFont("Segoe UI", 11))
        self.remove_field_entry.setStyleSheet(f"""
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
        self.remove_field_entry.setPlaceholderText("Enter field name to remove")
        remove_field_layout.addWidget(self.remove_field_entry)
        
        remove_field_help = QLabel("Enter the name of the field you want to remove")
        remove_field_help.setFont(QFont("Segoe UI", 9))
        remove_field_help.setStyleSheet(f"color: {colors['placeholder']};")
        remove_field_layout.addWidget(remove_field_help)
        
        remove_layout.addWidget(remove_field_container)
        
        # Warning message
        warning_container = QFrame()
        warning_container.setStyleSheet(f"""
            background-color: #fff8e6;
            border-radius: 4px;
        """)
        warning_layout = QHBoxLayout(warning_container)
        warning_layout.setContentsMargins(15, 15, 15, 15)
        warning_layout.setSpacing(10)
        
        warning_icon = QLabel("⚠️")
        warning_icon.setFont(QFont("Segoe UI", 14))
        warning_icon.setStyleSheet("background-color: transparent;")
        warning_layout.addWidget(warning_icon, 0, Qt.AlignmentFlag.AlignTop)
        
        warning_text = QLabel("This action cannot be undone. All data associated with this field will be permanently deleted.")
        warning_text.setFont(QFont("Segoe UI", 10))
        warning_text.setWordWrap(True)
        warning_text.setStyleSheet("color: #FBBF24; background-color: transparent;")
        warning_layout.addWidget(warning_text, 1)
        
        remove_layout.addWidget(warning_container)
        
        # Add spacer
        remove_layout.addStretch()
        
        # Remove button
        remove_field_btn = QPushButton("Remove Field")
        remove_field_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        remove_field_btn.setStyleSheet(f"""
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
        remove_field_btn.clicked.connect(self.remove_field)
        remove_layout.addWidget(remove_field_btn)
        
        main_layout.addWidget(main_container)
        
    def show_tab(self, index):
        self.tab_stack.setCurrentIndex(index)
        
        if index == 0:  # Add tab
            self.add_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['accent']};
                    color: white;
                    border-radius: 4px;
                    padding: 10px 20px;
                }}
                QPushButton:hover {{
                    background-color: #2563EB;
                }}
            """)
            self.remove_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['border']};
                    color: {self.colors['text']};
                    border-radius: 4px;
                    padding: 10px 20px;
                }}
                QPushButton:hover {{
                    background-color: #4B5563;
                }}
            """)
        else:  # Remove tab
            self.remove_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['accent']};
                    color: white;
                    border-radius: 4px;
                    padding: 10px 20px;
                }}
                QPushButton:hover {{
                    background-color: #2563EB;
                }}
            """)
            self.add_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['border']};
                    color: {self.colors['text']};
                    border-radius: 4px;
                    padding: 10px 20px;
                }}
                QPushButton:hover {{
                    background-color: #4B5563;
                }}
            """)
    
    def set_validation_type(self, value):
        self.validation_type = value
        
        # Update button styles to show selection
        for btn in self.validation_buttons:
            if (btn.text() == "String" and value == "string") or \
               (btn.text() == "Integer" and value == "int") or \
               (btn.text() == "Decimal" and value == "float"):
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.colors['accent']};
                        color: white;
                        border-radius: 4px;
                        padding: 10px 15px;
                    }}
                    QPushButton:hover {{
                        background-color: #2563EB;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.colors['border']};
                        color: {self.colors['text']};
                        border-radius: 4px;
                        padding: 10px 15px;
                    }}
                    QPushButton:hover {{
                        background-color: #d1d5db;
                    }}
                """)
    
    def set_required(self, value):
        self.required = value
        
        # Update button styles to show selection
        for btn in self.required_buttons:
            if (btn.text() == "Yes" and value == "1") or (btn.text() == "No" and value == "0"):
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.colors['accent']};
                        color: white;
                        border-radius: 4px;
                        padding: 10px 15px;
                    }}
                    QPushButton:hover {{
                        background-color: #2563EB;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.colors['border']};
                        color: {self.colors['text']};
                        border-radius: 4px;
                        padding: 10px 15px;
                    }}
                    QPushButton:hover {{
                        background-color: #d1d5db;
                    }}
                """)
    
    def add_field(self):
        field_name = self.field_name_entry.text().strip()
        
        if not field_name:
            QMessageBox.warning(self, "Input Error", "Field name cannot be empty.")
            return
        
        # Check if field already exists
        existing_fields = self.logic.get_existing_fields()
        if field_name.lower() in [f.lower() for f in existing_fields]:
            QMessageBox.warning(self, "Input Error", f"Field '{field_name}' already exists.")
            return
        
        # Add the field to the database with validation type and required status
        try:
            # Debug information
            print(f"Adding field: {field_name}")
            # Always use small_box as the entry type
            entry_type = "small_box"
            print(f"Entry type: {entry_type}")
            print(f"Validation type: {self.validation_type}")
            print(f"Required: {self.required}")
            
            # Make sure required is properly converted to integer
            required_int = 1 if self.required == "1" else 0
            print(f"Required as integer: {required_int}")
            
            # Use the selected validation type and required status with fixed entry_type
            # Pass required_int instead of self.required
            self.logic.add_field_to_database(field_name, entry_type, self.validation_type, required_int)
            
            QMessageBox.information(self, "Success", f"Field '{field_name}' added successfully.")
            self.field_name_entry.clear()
            
            # Reset to default values
            self.validation_type = "string"
            self.required = "1"
            
            # Update button styles to reflect defaults
            self.set_validation_type("string")
            self.set_required("1")
            
            # Refresh all views to show the new field
            if hasattr(self.parent(), 'refresh_views'):
                self.parent().refresh_views()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add field: {str(e)}")
            print(f"Error adding field: {str(e)}")
    
    def remove_field(self):
        field_name = self.remove_field_entry.text().strip()
        
        if not field_name:
            QMessageBox.warning(self, "Input Error", "Field name cannot be empty.")
            return
            
        # Check if field exists
        existing_fields = self.logic.get_existing_fields()
        if field_name not in existing_fields:
            QMessageBox.critical(self, "Error", f"Field '{field_name}' does not exist.")
            return
            
        # Define built-in fields that cannot be removed
        built_in_fields = ["brand", "category", "description", "id", "name", "price", "quantity"]
        
        if field_name.lower() in [f.lower() for f in built_in_fields]:
            QMessageBox.critical(self, "Error", f"'{field_name}' is a system field and cannot be removed.")
            return
            
        # Ask for confirmation
        confirm = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            f"Are you sure you want to remove the field '{field_name}'?\n\nThis will delete all associated data and cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                print(f"Removing field: {field_name}")
                
                # First, remove the field from the fields table
                self.inventory_system.remove_to_fields_table(field_name)
                
                # Then, remove the column from the items table
                try:
                    # Get all columns except the one to remove
                    self.inventory_system.cursor.execute(f"PRAGMA table_info({self.inventory_system.items_table})")
                    columns = [column[1] for column in self.inventory_system.cursor.fetchall() if column[1].lower() != field_name.lower()]
                    
                    # Create a new table without the column
                    columns_str = ", ".join(columns)
                    self.inventory_system.cursor.execute(f"CREATE TABLE temp_table AS SELECT {columns_str} FROM {self.inventory_system.items_table}")
                    
                    # Drop the old table
                    self.inventory_system.cursor.execute(f"DROP TABLE {self.inventory_system.items_table}")
                    
                    # Rename the new table
                    self.inventory_system.cursor.execute(f"ALTER TABLE temp_table RENAME TO {self.inventory_system.items_table}")
                    
                    # Commit the changes
                    self.inventory_system.conn.commit()
                    
                    print(f"Successfully removed column '{field_name}' from items table")
                except Exception as e:
                    print(f"Error removing column from items table: {str(e)}")
                    raise e
                
                QMessageBox.information(self, "Success", f"Field '{field_name}' removed successfully.")
                self.remove_field_entry.clear()
                
                # Refresh all views to reflect the removed field
                if hasattr(self.parent(), 'refresh_views'):
                    self.parent().refresh_views()
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove field: {str(e)}")
                print(f"Error removing field: {str(e)}")
    
    def refresh_fields(self):
        """Refresh the list of fields in the remove field dropdown"""
        if hasattr(self, 'remove_field_entry'):
            existing_fields = self.logic.get_existing_fields()
            # If this is a combobox, update its items
            if hasattr(self.remove_field_entry, 'clear') and hasattr(self.remove_field_entry, 'addItems'):
                self.remove_field_entry.clear()
                self.remove_field_entry.addItems(existing_fields)