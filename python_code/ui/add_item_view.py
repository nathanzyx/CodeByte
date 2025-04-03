from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QFrame, QMessageBox, QScrollArea, QWidget,
                            QGridLayout, QTextEdit, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QRegularExpressionValidator, QPixmap
from PyQt6.QtCore import QRegularExpression

class AddItemView(QWidget):  # Changed from QDialog to QWidget
    def __init__(self, parent, logic, inventory_system):
        super().__init__(parent)
        self.logic = logic
        self.inventory_system = inventory_system
        self.entries = {}
        self.message_labels = {}
        # Set dark background for all widgets and their children
        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
            }
            QFrame {
                background-color: #111827;
            }
            QLineEdit, QTextEdit {
                background-color: #1F2937;
            }
            QScrollArea {
                background-color: #111827;
            }
            QLabel {
                background-color: transparent;
            }
        """)
        self.setup_ui()
        
    # Update the color palette and styling for inputs and containers
    # Update the background color to match inventory view
    def setup_ui(self):
        # Get field specifications
        self.entries, self.message_labels, self.prod_specs = self.logic.get_add_item_specs(self)
        
        # Create a background frame that fills the entire widget
        background_frame = QFrame(self)
        background_frame.setStyleSheet("background-color: #1e1e1e;")
        background_frame.setGeometry(0, 0, self.width(), self.height())
        background_frame.setAutoFillBackground(True)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Update the color palette to match the dark theme from inventory view
        colors = {
            'primary': '#111827',     # Dark background
            'container_bg': '#1F2937', # Dark container background
            'input_bg': '#111827',    # Dark input background
            'text': '#E5E7EB',        # Light text for dark background
            'text_light': '#F9FAFB',  # Light text for dark backgrounds
            'accent': '#3B82F6',      # Blue accent
            'border': '#374151',      # Dark border
            'error': '#ef4444',       # Error red
            'placeholder': '#9ca3af', # Placeholder text
            'custom_bg': '#111827',   # Dark gray for custom fields
        }
        
        # Make sure the background frame stays full size when window resizes
        self.resizeEvent = lambda event: background_frame.setGeometry(0, 0, self.width(), self.height())
        
        # Set the background color for the main widget to match inventory view
        self.setStyleSheet(f"background-color: {colors['primary']};")
        
        # Add header section
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)
    
        title = QLabel("Add Product")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {colors['text_light']};")
        header_layout.addWidget(title)
    
        main_layout.addWidget(header_frame)
        
        # Create a main container with dark background and minimal borders
        main_container = QFrame()
        main_container.setStyleSheet(f"""
            background-color: {colors['container_bg']};
            border-radius: 8px;
            border: none;
        """)
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(20)
        
        # Create a grid layout for the form fields
        form_grid = QGridLayout()
        form_grid.setHorizontalSpacing(20)
        form_grid.setVerticalSpacing(20)
        
        # Define the fields we want to show in the grid
        field_positions = {
            'ID': (0, 0),
            'Name': (0, 1),
            'Brand': (1, 0),
            'Category': (1, 1),
            'Description': (2, 0),
            'Price': (2, 1),
            'Quantity': (3, 0),
        }
        
        # Define validation patterns for each field
        validation_patterns = {
            'ID': '^[a-zA-Z0-9]+$',  # Only letters and numbers
            'Name': '',  # Any text is valid
            'Brand': '^[a-zA-Z0-9 ]+$',  # Only letters, numbers and spaces
            'Category': '^[a-zA-Z0-9 ]+$',  # Only letters, numbers and spaces
            'Description': '',  # Any text is valid
            'Price': '^[0-9]+(\.[0-9]{1,2})?$',  # Numbers with optional decimal point
            'Quantity': '^[0-9]+$',  # Only whole numbers
        }
        
        # Define placeholder text for each field
        placeholder_texts = {
            'ID': "Enter product ID (letters & numbers only)",
            'Name': "Enter product name",
            'Brand': "Enter brand name (letters & numbers only)",
            'Category': "Enter category (letters & numbers only)",
            'Description': "Enter product description",
            'Price': "0.00",
            'Quantity': "0",
        }
        
        # Create form fields based on the layout in the image
        for field_name, position in field_positions.items():
            # Skip images field
            if(field_name == "images"):
                return
            
            row, col = position
            
            # Field container
            field_container = QFrame()
            field_layout = QVBoxLayout(field_container)
            field_layout.setContentsMargins(0, 0, 0, 0)
            field_layout.setSpacing(5)
            
            # Label and required indicator in one row
            label_container = QWidget()
            label_layout = QHBoxLayout(label_container)
            label_layout.setContentsMargins(0, 0, 0, 0)
            label_layout.setSpacing(5)
            
            field_label = QLabel(field_name)
            # Update field label styling
            field_label.setStyleSheet(f"color: {colors['text']};")
            field_label.setFont(QFont("Segoe UI", 10))
            label_layout.addWidget(field_label)
            label_layout.addStretch()
            
            field_layout.addWidget(label_container)
            
            # Input field
            if field_name == "Description":
                entry = QTextEdit()
                entry.setPlaceholderText(placeholder_texts[field_name])
                entry.setFixedHeight(100)
            elif field_name == "Quantity":
                entry = QLineEdit()
                entry.setPlaceholderText(placeholder_texts[field_name])
                entry.setMinimumWidth(200)
                
                # Add validator for quantity (integers only)
                if validation_patterns[field_name]:
                    validator = QRegularExpressionValidator(QRegularExpression(validation_patterns[field_name]))
                    entry.setValidator(validator)
                    
                entry.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid #e5e7eb;
                        border-radius: 4px;
                        padding: 8px;
                        background-color: white;
                        color: black;
                    }
                """)
            elif field_name == "Price":
                entry = QLineEdit()
                entry.setPlaceholderText(placeholder_texts[field_name])
                entry.setMinimumWidth(200)
                
                # Add validator for price (numbers with optional decimal)
                if validation_patterns[field_name]:
                    validator = QRegularExpressionValidator(QRegularExpression(validation_patterns[field_name]))
                    entry.setValidator(validator)
            else:
                entry = QLineEdit()
                entry.setPlaceholderText(placeholder_texts[field_name])
                entry.setMinimumWidth(200)
                
                # Add validators for other fields
                if validation_patterns[field_name]:
                    validator = QRegularExpressionValidator(QRegularExpression(validation_patterns[field_name]))
                    entry.setValidator(validator)
            
            # Style the input fields with dark theme
            if isinstance(entry, QLineEdit):
                entry.setStyleSheet(f"""
                    QLineEdit {{
                        border: 1px solid {colors['border']};
                        border-radius: 4px;
                        padding: 8px;
                        background-color: {colors['input_bg']};
                        color: {colors['text']};
                    }}
                    QLineEdit:focus {{
                        border: 1px solid {colors['accent']};
                    }}
                """)
            else:  # QTextEdit
                entry.setStyleSheet(f"""
                    QTextEdit {{
                        border: 1px solid {colors['border']};
                        border-radius: 4px;
                        padding: 8px;
                        background-color: {colors['input_bg']};
                        color: {colors['text']};
                    }}
                    QTextEdit:focus {{
                        border: 1px solid {colors['accent']};
                    }}
                """)
            
            field_layout.addWidget(entry)
            
            # Error message label (hidden initially)
            message_label = QLabel("")
            message_label.setStyleSheet(f"color: {colors['error']}; font-size: 9px;")
            field_layout.addWidget(message_label)
            
            # Store references for validation
            validation_type = 'text'
            if field_name == 'Price':
                validation_type = 'float'
            elif field_name == 'Quantity':
                validation_type = 'int'
            elif field_name == 'ID':
                validation_type = 'alphanumeric'
            elif field_name == 'Brand' or field_name == 'Category':
                validation_type = 'alphanumeric_space'
                
            self.entries[field_name] = (entry, validation_type, field_name != "Description")
            self.message_labels[field_name] = message_label
            
            form_grid.addWidget(field_container, row, col)
        
        container_layout.addLayout(form_grid)
        
        # Bottom section with image upload and custom fields
        bottom_container = QHBoxLayout()
        bottom_container.setSpacing(20)
        
        # Image upload section
        image_container = QFrame()
        image_container.setStyleSheet(f"""
            background-color: {colors['input_bg']};
            border-radius: 4px;
            border: 1px solid {colors['border']};
        """)
        # Create a vertical layout for the image container to hold the images
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(10, 10, 10, 10)
        image_container_layout.setSpacing(10)
        # Make upload label for the top
        self.upload_label = QLabel("Click to Upload Image")
        self.upload_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_label.setStyleSheet(f"color: {colors['text']}; font-size: 14px; font-weight: bold;")
        self.upload_label.mousePressEvent = self.upload_image  # Make it clickable
        image_container_layout.addWidget(self.upload_label)
        # Wdiget to hold the images
        self.image_list_widget = QWidget()
        self.image_layout = QVBoxLayout(self.image_list_widget)
        self.image_layout.setContentsMargins(5, 5, 5, 5)
        self.image_layout.setSpacing(10)
        # Scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_list_widget)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background: {colors['primary']};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #4B5563;
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        image_container_layout.addWidget(scroll_area)
        bottom_container.addWidget(image_container)
        
        
        
        
        # Custom fields section (right)
        custom_fields_container = QFrame()
        custom_fields_container.setStyleSheet(f"""
            background-color: {colors['input_bg']};
            border-radius: 4px;
        """)
        custom_fields_layout = QVBoxLayout(custom_fields_container)
        custom_fields_layout.setContentsMargins(10, 10, 10, 10)
        
        custom_fields_title = QLabel("Custom Fields")
        custom_fields_title.setStyleSheet(f"color: {colors['text']}; font-weight: bold; border: none;")
        custom_fields_layout.addWidget(custom_fields_title)
        
        # Create a scroll area for custom fields
        custom_fields_scroll = QScrollArea()
        custom_fields_scroll.setWidgetResizable(True)
        custom_fields_scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {colors['primary']};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #4B5563;
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Create a widget to hold the list of custom fields
        custom_fields_list = QWidget()
        custom_fields_list_layout = QVBoxLayout(custom_fields_list)
        custom_fields_list_layout.setContentsMargins(0, 0, 0, 0)
        custom_fields_list_layout.setSpacing(8)
        
        # Get custom fields from the database with better error handling
        try:
            # Check if the method exists first
            if hasattr(self.logic, 'get_existing_fields'):
                # Get all fields
                all_fields = self.logic.get_existing_fields()
                
                # Debug: Print the type and content of all_fields
                print(f"Type of all_fields: {type(all_fields)}")
                print(f"Content of all_fields: {all_fields}")
                
                # Define standard fields that should be excluded
                standard_fields = ['id', 'name', 'brand', 'category', 'description', 'price', 'quantity', 'images']
                
                # Check if we have fields to process
                if all_fields:
                    # Handle different possible formats of all_fields
                    if isinstance(all_fields, list):
                        # If all_fields is a list of strings (field names)
                        if all_fields and isinstance(all_fields[0], str):
                            # Only include fields that are not in standard_fields (case-insensitive)
                            custom_fields = [field for field in all_fields if field.lower() not in standard_fields]
                            
                            if custom_fields:
                                for field_name in custom_fields:
                                    field_container = QFrame()
                                    field_layout = QVBoxLayout(field_container)
                                    field_layout.setContentsMargins(0, 0, 0, 0)
                                    field_layout.setSpacing(4)
                                    
                                    # Label with field type
                                    label_container = QWidget()
                                    label_layout = QHBoxLayout(label_container)
                                    label_layout.setContentsMargins(0, 0, 0, 0)
                                    
                                    field_label = QLabel(field_name)
                                    field_label.setStyleSheet("color: white;")
                                    label_layout.addWidget(field_label)
                                    label_layout.addStretch()
                                    
                                    # Removed the required label here
                                    
                                    field_layout.addWidget(label_container)
                                    
                                    # Input field (default to small_box)
                                    field_input = QLineEdit()
                                    field_input.setPlaceholderText("Input text")
                                    field_input.setStyleSheet(f"""
                                        QLineEdit {{
                                            border: 1px solid {colors['border']};
                                            border-radius: 4px;
                                            padding: 8px;
                                            background-color: {colors['input_bg']};
                                            color: {colors['text']};
                                        }}
                                        QLineEdit:focus {{
                                            border: 1px solid {colors['accent']};
                                        }}
                                    """)
                                    
                                    field_layout.addWidget(field_input)
                                    
                                    # Error message label
                                    message_label = QLabel("")
                                    message_label.setStyleSheet("color: #ef4444; font-size: 9px;")
                                    field_layout.addWidget(message_label)
                                    
                                    # Get field details from database
                                    validation_type = 'text'  # Default
                                    is_required = False  # Default
                                    
                                    try:
                                        if hasattr(self.logic, 'get_field_details'):
                                            field_details = self.logic.get_field_details(field_name)
                                            if field_details:
                                                # Extract validation type and required status
                                                if 'validation_type' in field_details:
                                                    validation_type = field_details['validation_type']
                                                if 'required' in field_details:
                                                    is_required = field_details['required'] == '1'
                                    except Exception as e:
                                        print(f"Error getting field details: {str(e)}")
                                        # Continue with defaults if there's an error
                                    
                                    # Store references for validation with correct validation type
                                    self.entries[field_name] = (field_input, validation_type, is_required)
                                    self.message_labels[field_name] = message_label
                                    
                                    custom_fields_list_layout.addWidget(field_container)
                            else:
                                # No custom fields found after filtering
                                no_fields_label = QLabel("No custom fields available. Add fields in Manage Fields.")
                                no_fields_label.setStyleSheet(f"color: {colors['placeholder']}; font-style: italic;")
                                no_fields_label.setWordWrap(True)
                                custom_fields_list_layout.addWidget(no_fields_label)
                        else:
                            # Unknown list format
                            error_label = QLabel("Unknown list format for fields. Please check the data source.")
                            error_label.setStyleSheet(f"color: {colors['error']}; font-style: italic;")
                            error_label.setWordWrap(True)
                            custom_fields_list_layout.addWidget(error_label)
                    else:
                        # Unknown format
                        error_label = QLabel(f"Unexpected data format for fields: {type(all_fields)}. Please check the data source.")
                        error_label.setStyleSheet("color: #ef4444; font-style: italic;")
                        error_label.setWordWrap(True)
                        custom_fields_list_layout.addWidget(error_label)
                else:
                    # all_fields is empty or None
                    no_fields_label = QLabel("No fields found in the system. Please set up fields first.")
                    no_fields_label.setStyleSheet("color: #6b7280; font-style: italic;")
                    no_fields_label.setWordWrap(True)
                    custom_fields_list_layout.addWidget(no_fields_label)
            else:
                # Method doesn't exist
                method_error_label = QLabel("System error: get_existing_fields method not found.")
                method_error_label.setStyleSheet("color: #ef4444; font-style: italic;")
                method_error_label.setWordWrap(True)
                custom_fields_list_layout.addWidget(method_error_label)
                
                # Fallback to display a placeholder
                placeholder_label = QLabel("Custom fields will appear here once configured.")
                placeholder_label.setStyleSheet(f"color: {colors['placeholder']}; margin-top: 10px;")
                placeholder_label.setWordWrap(True)
                custom_fields_list_layout.addWidget(placeholder_label)
                
        except Exception as e:
            # Handle any errors that might occur when getting fields
            import traceback
            error_details = traceback.format_exc()
            
            error_label = QLabel(f"Could not load custom fields: {str(e)}")
            error_label.setStyleSheet("color: #ef4444; font-style: italic;")
            error_label.setWordWrap(True)
            custom_fields_list_layout.addWidget(error_label)
            
            # Add a placeholder message
            placeholder_label = QLabel("Custom fields will appear here once the issue is resolved.")
            placeholder_label.setStyleSheet("color: #6b7280; margin-top: 10px;")
            placeholder_label.setWordWrap(True)
            custom_fields_list_layout.addWidget(placeholder_label)
            
            # Print detailed error to console for debugging
            print(f"Error loading custom fields: {str(e)}")
            print(error_details)
        
        # Add stretch to push everything to the top
        custom_fields_list_layout.addStretch()
        
        # Set the custom fields list as the scroll area widget
        custom_fields_scroll.setWidget(custom_fields_list)
        custom_fields_layout.addWidget(custom_fields_scroll)
        
        bottom_container.addWidget(custom_fields_container)
        
        container_layout.addLayout(bottom_container)
        
        # Add item button
        submit_btn = QPushButton("Add Item")
        submit_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border-radius: 4px;
                padding: 10px 0;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        submit_btn.clicked.connect(self.add_item_submit)
        container_layout.addWidget(submit_btn)
        
        main_layout.addWidget(main_container)
    
    
    def upload_image(self, event):
    
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Image files (*.png *.jpg *.jpeg *.bmp *.gif)"]) # Types of files we allow for upload
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)  # Allow selecting multiple files

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()  # Get the list of selected image paths for validation

            # make image paths list if it doesn't exist
            if not hasattr(self, "image_paths"):
                self.image_paths = []

            # Add the new images to the list
            for image_path in selected_files:
                #Ensure image path does not already exist in the list to avoid duplicates
                if image_path not in self.image_paths:
                    self.image_paths.append(image_path)

            # Refresh image container to display the updated list of images
            self.refresh_image_container()
            
            
    def refresh_image_container(self):
        # Clear the current layout in the scroll area
        while self.image_layout.count():
            child = self.image_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # For each image, create a container with the remove button and thumbnail
        for image_path in self.image_paths:
            image_item_container = QFrame()
            image_item_layout = QHBoxLayout(image_item_container)
            image_item_layout.setContentsMargins(5, 5, 5, 5)
            image_item_layout.setSpacing(10)

            # Remove button on the left
            remove_button = QPushButton("Remove")
            remove_button.setFixedSize(80, 30)
            remove_button.setStyleSheet("""
                QPushButton {
                    background-color: #EF4444;;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #DC2626;
                }
            """
            )
            remove_button.clicked.connect(lambda _, path=image_path: self.remove_image(path))
            image_item_layout.addWidget(remove_button)

            # Thumbnail for the iamge
            pixmap = QPixmap(image_path)
            thumbnail = QLabel()
            thumbnail.setPixmap(pixmap.scaled(
                80, 80,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
            thumbnail.setStyleSheet("border: 0px solid #374151; margin: 5px;")
            image_item_layout.addWidget(thumbnail)

            # Add image item container to the layout
            self.image_layout.addWidget(image_item_container)

        # Stretch at the end to push the items upward
        self.image_layout.addStretch()
    
    #
    # Removes an image from the list
    #
    def remove_image(self, image_path):
        if hasattr(self, "image_paths") and image_path in self.image_paths:
            self.image_paths.remove(image_path)
            self.refresh_image_container()
        
    def cancel_action(self):
        # Go back to the default view
        parent = self.parent()
        while parent and not hasattr(parent, 'stacked_widget'):
            parent = parent.parent()
        
        if parent and hasattr(parent, 'stacked_widget'):
            parent.stacked_widget.setCurrentWidget(parent.default_view)
    
    #
    #   Clear the images from the UI container and List
    #
    def clear_images(self):
        # Clear the image paths
        self.image_paths = []

        # Remove all widgets from the image container
        while self.image_layout.count():
            child = self.image_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    def add_item_submit(self):
        # Clear previous error messages
        for label in self.message_labels:
            self.message_labels[label].setText("")
            
        # Get the ID value first to check for duplicates
        id_entry = self.entries.get('ID', (None, None, None))[0]
        if id_entry:
            new_id = id_entry.text().strip()
            # Check if ID already exists
            existing_items = self.inventory_system.get_all_items()
            if new_id in existing_items['id'].values:
                self.message_labels['ID'].setText("This ID already exists")
                self.message_labels['ID'].setStyleSheet("color: #ef4444;")
                return

        # Rest of the validation and submission code
        validation_passed = True
        product_data = {}
        
        # Get the exact field names from the database to preserve case
        self.inventory_system.cursor.execute(f"SELECT field_name, required FROM {self.inventory_system.fields_table}")
        db_field_info = {row[0]: bool(row[1]) for row in self.inventory_system.cursor.fetchall()}
        db_field_names_map = {name.lower(): name for name in db_field_info.keys()}
        
        for label, (entry, validation_type, is_required) in self.entries.items():
            # Get the value depending on entry type
            if isinstance(entry, QTextEdit):
                value = entry.toPlainText()
            else:
                value = entry.text()
                
            # Get the actual field name from database (preserving case)
            db_field_name = db_field_names_map.get(label.lower(), label)
            
            # Get the required status directly from the database
            is_required = db_field_info.get(db_field_name, False)
                
            # Check if required field is empty
            if is_required and not value.strip():
                validation_passed = False
                self.message_labels[label].setText(f"{label} is required")
                self.message_labels[label].setStyleSheet("color: #ef4444;")  # Red error text
                continue
                
            # Add custom field validations based on field type
            valid = True
            error_msg = ""
            
            if value.strip():  # Only validate if there's input
                if validation_type == 'alphanumeric':
                    if not value.strip().isalnum():
                        valid = False
                        error_msg = f"{label} must contain only letters and numbers"
                elif validation_type == 'alphanumeric_space':
                    if not all(c.isalnum() or c.isspace() for c in value):
                        valid = False
                        error_msg = f"{label} must contain only letters, numbers and spaces"
                elif validation_type == 'int':
                    try:
                        int(value)
                    except ValueError:
                        valid = False
                        error_msg = f"{label} must be a whole number"
                elif validation_type == 'float':
                    try:
                        float(value)
                        # Check for proper decimal format
                        if '.' in value:
                            integer_part, decimal_part = value.split('.')
                            if not integer_part.isdigit() or not decimal_part.isdigit():
                                valid = False
                                error_msg = f"{label} must be a number with valid decimal"
                    except ValueError:
                        valid = False
                        error_msg = f"{label} must be a valid number"
            
            if not valid:
                validation_passed = False
                self.message_labels[label].setText(error_msg)
                self.message_labels[label].setStyleSheet("color: #ef4444;")  # Red error text
            else:
                # Use the exact field name from the database
                product_data[db_field_name] = value
        
        if not validation_passed:
            return
        
        if hasattr(self, "image_paths") and self.image_paths:
            product_data["images"] = self.image_paths  # Add the list of image paths to the product data list
        
        try:
            # Make sure all required fields are present (case-insensitive check)
            required_fields = ['id', 'name', 'quantity', 'price', 'category', 'brand', 'description']
            product_data_lower = {k.lower(): v for k, v in product_data.items()}
            missing_fields = [field for field in required_fields if field not in product_data_lower]
            
            if missing_fields:
                QMessageBox.warning(self, "Missing Fields", f"The following required fields are missing: {', '.join(missing_fields)}")
                return
            
            # Add the item to the database
            success = self.inventory_system.add_item_to_database(product_data)
            
            if success is False:  # Explicitly check for False, not None or other falsy values
                QMessageBox.warning(self, "Error", "Failed to add item to database.")
                return
                
            # Clear form fields after successful submission
            for label, (entry, _, _) in self.entries.items():
                if isinstance(entry, QTextEdit):
                    entry.clear()
                else:
                    entry.clear()
            # Clear The Images
            self.clear_images()
                
            QMessageBox.information(self, "Success", "Item added successfully.")
            
            # Go back to the default view
            parent = self.parent()
            while parent and not hasattr(parent, 'stacked_widget'):
                parent = parent.parent()
            
            if parent and hasattr(parent, 'stacked_widget'):
                # Refresh the inventory view before switching to it
                if hasattr(parent, 'inventory_view'):
                    parent.inventory_view.display_all_items()
                parent.stacked_widget.setCurrentWidget(parent.inventory_view)  # Go directly to inventory view
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add item: {str(e)}")
            
            