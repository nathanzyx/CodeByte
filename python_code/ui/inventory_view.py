from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
                            QPushButton, QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QMessageBox, QDialog, QFormLayout, QListWidget, 
                            QListWidgetItem, QCheckBox, QScrollArea, QComboBox, QSizePolicy, QFileDialog, QStackedWidget)
from PyQt6.QtCore import Qt, QRegularExpression, QTimer
from PyQt6.QtGui import QFont, QIcon, QColor, QRegularExpressionValidator, QPixmap, QBrush, QMovie
import pandas as pd
import re
import os  # Add this import

class InventoryView(QMainWindow):
    def __init__(self, parent, inventory_system, ai):
        super().__init__(parent)
        self.inventory_system = inventory_system
        self.ai = ai
        self.selected_fields = set()
        
        # Define the normal style (For Normal search results)
        self.normal_style = ("""
            QTableWidget {
                border: none;
                gridline-color: #374151;
                background-color: #1F2937;
                color: #E5E7EB;
                alternate-background-color: #111827;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #374151;
            }
            QTableWidget::item:selected {
                background-color: #3B82F6;
                color: white;
            }
            QHeaderView::section {
                background-color: #111827;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #374151;
                font-weight: bold;
                color: #9CA3AF;
                text-transform: uppercase;
            }
            QScrollBar:vertical {
                border: none;
                background: #1F2937;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4B5563;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        # Define the ai recommended items style
        self.ai_style = ("""
            QTableWidget {
                border: none;
                gridline-color: #374151;
                background-color: #1F2937;
                color: #ff6d45;
                alternate-background-color: #111827;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #374151;
            }
            QTableWidget::item:selected {
                background-color: #3B82F6;
                color: white;
            }
            QHeaderView::section {
                background-color: #111827;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #374151;
                font-weight: bold;
                color: #9CA3AF;
                text-transform: uppercase;
            }
            QScrollBar:vertical {
                border: none;
                background: #1F2937;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4B5563;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.setup_ui()
        
        
        # FOR AI RECOMMENDATION
        self.ai_recommendation_timer = QTimer(self)  # Timer to delay AI call (prevents constant AI calls)
        self.ai_recommendation_timer.setSingleShot(True)
        self.last_search_query = ""  # Store the last search query so it can later be sent to the AI
        self.ai_recommendation_timer.timeout.connect(self.fetch_ai_recommendations) # AI will be called after the timer expires

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Set the background color for the main widget
        central_widget.setStyleSheet("background-color: #1e1e1e;")

        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)

        title = QLabel("Inventory Management")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #F9FAFB;")
        header_layout.addWidget(title)

        main_layout.addWidget(header_frame)

        # Search bar and buttons
        search_container = QFrame()
        search_container.setStyleSheet("""
            background-color: #1F2937;
            border-radius: 4px;
            border: 1px solid #374151;
        """)
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(16, 16, 16, 16)
        search_layout.setSpacing(12)
        
        self.search_entry = QLineEdit()
        self.search_entry.setFont(QFont("Segoe UI", 11))
        self.search_entry.setPlaceholderText("Search inventory...")
        self.search_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #374151;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: #111827;
                color: #E5E7EB;
            }
            QLineEdit:focus {
                border: 1px solid #3B82F6;
            }
        """)
        self.search_entry.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_entry, 1)  # Give search bar more space
        
        # Filter button with blue styling
        self.filter_button = QPushButton("Filters")
        self.filter_button.setFont(QFont("Segoe UI", 11))
        self.filter_button.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                border: 1px solid #2563EB;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        self.filter_button.clicked.connect(self.toggle_filter_section)
        search_layout.addWidget(self.filter_button)
        
        # Search button removed since search happens automatically
        
        main_layout.addWidget(search_container)
        
        # Filter section (hidden by default)
        self.filter_section = QFrame()
        self.filter_section.setVisible(False)
        self.filter_section.setStyleSheet("""
            background-color: #1F2937;
            border-radius: 4px;
            border: none;
        """)
        filter_layout = QVBoxLayout(self.filter_section)
        filter_layout.setContentsMargins(16, 16, 16, 16)
        filter_layout.setSpacing(12)
        
        filter_title = QLabel("Filter Options")
        filter_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        filter_title.setStyleSheet("""
            color: #F9FAFB;
            border: 1px solid #374151;
            border-radius: 4px;
            padding: 8px;
            background-color: #111827;
        """)
        filter_layout.addWidget(filter_title)
        
        # Field checkboxes
        checkbox_container = QWidget()
        checkbox_layout = QVBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setSpacing(8)
        
        self.field_checkboxes = {}
        
        # Get all fields from the DataFrame
        df = self.inventory_system.get_all_items()
        all_fields = df.columns.tolist()
        
        # grid layout for field checkboxes (removed Select All checkbox)
        fields_grid = QWidget()
        fields_grid_layout = QGridLayout(fields_grid)
        fields_grid_layout.setContentsMargins(0, 0, 0, 0)
        fields_grid_layout.setSpacing(8)
        
        # Add field checkboxes in a grid
        columns_per_row = 3
        for idx, field in enumerate(all_fields):
            checkbox = QCheckBox(field.capitalize())
            checkbox.setFont(QFont("Segoe UI", 11))
            checkbox.setStyleSheet("""
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
            checkbox.setChecked(True)  # All fields selected by default
            checkbox.stateChanged.connect(self.on_field_selection_changed)
            
            row = idx // columns_per_row
            col = idx % columns_per_row
            fields_grid_layout.addWidget(checkbox, row, col)
            self.field_checkboxes[field] = checkbox
            
        checkbox_layout.addWidget(fields_grid)
        filter_layout.addWidget(checkbox_container)
        
        # Stacked widget for the legend and no recommendations message -----------------------------------
        self.legend_stack = QStackedWidget()

        # "Recommended" legend
        self.legend_label = QLabel("🟠 Recommended")
        self.legend_label.setStyleSheet("color: #ff6d45; font-size: 12px; font-weight: bold;")
        self.legend_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.legend_stack.addWidget(self.legend_label)  # Add to stacked widget

        # "No Recommendations" message
        self.no_recommendations_label = QLabel("No similar items found.")
        self.no_recommendations_label.setStyleSheet("color: #8c9aa8; font-size: 12px; font-weight: bold;")
        self.no_recommendations_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.legend_stack.addWidget(self.no_recommendations_label)  # Add to stacked widget
        
        # Empty message
        self.empty_label = QLabel("")
        self.empty_label.setStyleSheet("color: #ffffff; font-size: 12px; font-weight: bold;")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.legend_stack.addWidget(self.empty_label)  # Add to stacked widget

        # Initially show the EMpty
        self.legend_stack.setCurrentWidget(self.empty_label)

        # Add the stacked widget to the layout
        main_layout.addWidget(self.legend_stack)

        # Table section -------------------------------------
        table_container = QFrame()
        table_container.setStyleSheet("""
            background-color: #1F2937;
            border-radius: 4px;
            border: 1px solid #374151;
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(16, 16, 16, 16)

        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet(self.normal_style)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.on_table_double_click)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.table.setAlternatingRowColors(True)
        
        table_layout.addWidget(self.table)
        main_layout.addWidget(table_container, 1)  # Give table more stretch

        self.display_all_items()

    def get_unique_categories(self):
        """Get unique categories from inventory data"""
        try:
            df = self.inventory_system.get_all_items()
            if 'category' in df.columns:
                return sorted(df['category'].unique().tolist())
            return []
        except:
            return []

    def on_field_selection_changed(self):
        """Update search results when field selection changes"""
        self.selected_fields = {field for field, checkbox in self.field_checkboxes.items() 
                               if checkbox.isChecked()}
        self.on_search()

    def refresh_fields(self):
        """Refresh the table and field checkboxes to show updated fields"""
        # Get current fields from database
        df = self.inventory_system.get_all_items()
        current_fields = df.columns.tolist()
        
        # Find the fields grid widget
        checkbox_container = self.filter_section.findChild(QWidget)
        if checkbox_container:
            fields_grid = checkbox_container.findChild(QWidget)
            if fields_grid and fields_grid.layout():
                # Clear existing checkboxes
                for i in reversed(range(fields_grid.layout().count())): 
                    fields_grid.layout().itemAt(i).widget().deleteLater()
                
                # Recreate field checkboxes
                columns_per_row = 3
                for idx, field in enumerate(current_fields):
                    checkbox = QCheckBox(field.capitalize())
                    checkbox.setFont(QFont("Segoe UI", 11))
                    checkbox.setStyleSheet("""
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
                    checkbox.setChecked(True)  # All fields selected by default
                    checkbox.stateChanged.connect(self.on_field_selection_changed)
                    
                    row = idx // columns_per_row
                    col = idx % columns_per_row
                    fields_grid.layout().addWidget(checkbox, row, col)
                    self.field_checkboxes[field] = checkbox
        
        # Update table with a search
        self.on_search()

    def on_search(self):
        self.legend_stack.setCurrentWidget(self.empty_label)
        query = self.search_entry.text()
        
        # Get all items
        df = self.inventory_system.get_all_items()
        
        # Get selected fields for filtering
        selected_fields = [field for field, checkbox in self.field_checkboxes.items() 
                          if checkbox.isChecked()]
        
        # Apply text search filter
        if query:
            # Escape special regex characters in the query
            escaped_query = re.escape(query)
            
            # If specific fields are selected, only search in those fields
            if selected_fields:
                mask = pd.Series(False, index=df.index)
                for field in selected_fields:
                    if field in df.columns:
                        mask |= df[field].astype(str).str.contains(escaped_query, case=False, na=False, regex=True)
                df = df[mask]
            else:
                # If no fields selected show nothing
                df = df.iloc[0:0]
                
        if df.empty: # If serach result yeilds no results
            self.update_table(df) # Clear the table (to show no results)
            self.last_search_query = query # Store the query as the last query so it can be sent to the AI if needed
            self.ai_recommendation_timer.start(1000) # Delay AI call by 1 second (To prevent constant AI API calls)
        else:
            self.ai_recommendation_timer.stop()  # Stop any pending AI calls
        self.update_table(df)
        
    #
    #   Creates and receives the AI API call
    #
    def fetch_ai_recommendations(self):
        try:
            # Call the make_Query function to get recommendations from the AI
            ai_recommendations_df = self.ai.make_Query(f"You MUST use the function 'show_ids' in your response, the user has searched for '{self.last_search_query}', and has not found anything matching their search, use the function to show the user 0 to 5 items that are similar to what the user has searched for. If there are no items in the database that are similar to what the user has searched for, return the function with an empty list i.e.: 'show_ids: []'")

            # Check if AI did not recommend any items
            if ai_recommendations_df.empty:
                self.legend_stack.setCurrentWidget(self.no_recommendations_label) # Make indicator visible that no similar items found
                return

            # Display the AI-recommended products in the table with highlighted rows
            self.legend_stack.setCurrentWidget(self.legend_label)
            self.update_table(ai_recommendations_df, ai_reccommended=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch AI recommendations: {str(e)}")
    
    def on_table_double_click(self, index):
        row = index.row()
        # Get all column headers
        headers = []
        for col in range(self.table.columnCount()):
            headers.append(self.table.horizontalHeaderItem(col).text())
            
        # Get data for all columns
        item_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
        self.modify_item(item_data, headers)
        
        
    def display_all_items(self):
        self.legend_stack.setCurrentWidget(self.empty_label)
        # Get all items as a DataFrame
        items_df = self.inventory_system.get_all_items()
        
        # Update the table with all items
        self.update_table(items_df)
        
        
        
    def update_table(self, df, ai_reccommended=False):
        # Clear the current table
        self.table.setRowCount(0)
        
        if df.empty:
            return
            
        # Set up table columns
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        
        if ai_reccommended:
            self.table.setStyleSheet(self.ai_style)
            self.table.setAlternatingRowColors(True)
        else:
            self.table.setStyleSheet(self.normal_style)
            self.table.setAlternatingRowColors(True)
        
        # Add items to table
        for row_idx, (_, row_data) in enumerate(df.iterrows()):
            self.table.insertRow(row_idx)
            for col_idx, field in enumerate(df.columns):
                value = row_data[field]
                item = QTableWidgetItem(str(value))
                    
                # self.table.setItem(row_idx, col_idx, item)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setBackground(QBrush(QColor('#1f7cff')))
                self.table.setItem(row_idx, col_idx, item)
        
        # Set column resize mode based on number of columns
        if len(df.columns) <= 7:
            # If 7 or fewer columns, stretch to fill the width
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        else:
            # If more than 7 columns, use fixed width with scrollbar
            for i in range(len(df.columns)):
                self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)    
        
    
    def modify_item(self, item_data, columns):
        if not item_data:
            return

        # Initialize dialog
        mod_dialog = QDialog(self)
        mod_dialog.setWindowTitle("Modify Product")
        mod_dialog.resize(900, 600)  # Wider dialog to accommodate side-by-side layout
        mod_dialog.setStyleSheet("""
            QDialog {
                background-color: #1F2937;
            }
            QLabel {
                font-weight: bold;
                color: #F9FAFB;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QLineEdit {
                border: 1px solid #374151;
                border-radius: 4px;
                padding: 8px;
                background-color: #111827;
                color: #E5E7EB;
            }
            QLineEdit:focus {
                border: 1px solid #3B82F6;
            }
        """)

        # Main layout (horizontal)
        main_layout = QHBoxLayout(mod_dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side (form fields)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 10, 20)
        left_layout.setSpacing(15)

        # Right side (images)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 20, 20, 20)
        right_layout.setSpacing(15)

        # Set panel widths
        left_panel.setMinimumWidth(500)
        right_panel.setMinimumWidth(300)

        # Title - Left panel
        title = QLabel("Edit Product Details")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        left_layout.addWidget(title)

        # Form layout for product details
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        entries = {}
        message_labels = {}

        # Populate fields
        for idx, col in enumerate(columns):
            label = QLabel(col.capitalize())
            label.setFont(QFont("Segoe UI", 12))

            entry = QLineEdit()
            entry.setFont(QFont("Segoe UI", 12))
            entry.setText(str(item_data[idx]))

            form_layout.addRow(label, entry)
            entries[col] = entry

            # Add error message label
            error_label = QLabel("")
            error_label.setStyleSheet("color: #ef4444; font-weight: normal; font-size: 10px;")
            form_layout.addRow("", error_label)
            message_labels[col] = error_label

        left_layout.addLayout(form_layout)
        
        # Add buttons to the bottom of left panel
        button_container = QFrame()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 0)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 12))
        cancel_btn.setStyleSheet("""
            background-color: #F1F5F9;
            color: #334155;
        """)
        cancel_btn.clicked.connect(mod_dialog.reject)

        save_btn = QPushButton("Save Changes")
        save_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        save_btn.clicked.connect(lambda: self.save_changes(mod_dialog, columns, entries, item_data, message_labels))

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        left_layout.addWidget(button_container)
        
        # Add spacer to push content up
        left_layout.addStretch()

        # Image section title - Right panel
        image_title = QLabel("Product Images")
        image_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        right_layout.addWidget(image_title)

        # Image frame
        image_container = QFrame()
        image_container.setStyleSheet("""
            background-color: #111827;
            border-radius: 4px;
            border: 1px solid #374151;
        """)

        # Layout for image container
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(10, 10, 10, 10)
        image_container_layout.setSpacing(10)

        # Upload button at the top of image section
        upload_btn = QPushButton("➕ Upload Images")
        upload_btn.setFont(QFont("Segoe UI", 12))
        upload_btn.setStyleSheet("""
            background-color: #3B82F6;
            color: white;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            text-align: center;
        """)
        upload_btn.clicked.connect(self.upload_image)
        image_container_layout.addWidget(upload_btn)

        # Scroll area for images
        self.image_list_widget = QWidget()
        self.image_layout = QVBoxLayout(self.image_list_widget)
        self.image_layout.setContentsMargins(5, 5, 5, 5)
        self.image_layout.setSpacing(10)
        self.image_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Keep images at the top

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_list_widget)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #111827;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4B5563;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        image_container_layout.addWidget(scroll_area)
        right_layout.addWidget(image_container, 1)  # Give it stretch to fill available space

        # Add help text at the bottom of image panel
        help_text = QLabel("Click 'Upload Images' to add product photos.\nYou can remove images by clicking the Remove button.")
        help_text.setStyleSheet("color: #9CA3AF; font-size: 11px; font-weight: normal;")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(help_text)

        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        # Load existing images
        self.load_existing_images(item_data[0])  # Pass the product ID

        mod_dialog.exec()

    #
    #   Loads existing images from the product into the list in the UI
    #
    def load_existing_images(self, product_id):
        self.existing_images = self.inventory_system.get_images_for_product(product_id)  # Retrieve images from the database
        self.image_paths = []  # Reset new image paths

        for image_data in self.existing_images:
            self.add_image_to_container(image_data, is_existing=True)
                        
    #
    #   Uploads a file to the UI list
    #
    def upload_image(self, event):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Image files (*.png *.jpg *.jpeg *.bmp *.gif)"])
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            for image_path in selected_files:
                if image_path not in self.image_paths:  # Avoid duplicates
                    self.image_paths.append(image_path)
                    self.add_image_to_container(image_path)

    #
    #   Add image to the image container list in the UI
    #       - as binary or an image path
    #
    def add_image_to_container(self, image_data, is_existing=False):
        image_item_container = QFrame()
        image_item_container.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 4px;
                border: 1px solid #374151;
                margin: 2px;
            }
        """)
        image_item_layout = QHBoxLayout(image_item_container)
        image_item_layout.setContentsMargins(8, 8, 8, 8)
        image_item_layout.setSpacing(10)

        # Thumbnail
        thumbnail = QLabel()
        pixmap = QPixmap()
        
        # Load from binary data or map depending if the image exists already
        if is_existing:
            pixmap.loadFromData(image_data)  # Load from binary
        else:
            pixmap.load(image_data)  # Load from path
            
        # Create a square thumbnail with fixed size    
        thumbnail.setPixmap(pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        thumbnail.setStyleSheet("border: none; background-color: transparent;")
        thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_item_layout.addWidget(thumbnail)

        # Add image name/info in the middle
        info_label = QLabel("Image")
        if not is_existing and image_data:
            # Show filename for new images
            file_name = os.path.basename(image_data)
            if len(file_name) > 20:
                file_name = file_name[:17] + "..."
            info_label.setText(file_name)
        info_label.setStyleSheet("color: #E5E7EB; font-size: 12px;")
        image_item_layout.addWidget(info_label, 1)  # Give it stretch

        # Remove button on the right
        remove_button = QPushButton("Remove")
        remove_button.setFixedSize(70, 30)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        remove_button.clicked.connect(lambda: self.remove_image(image_item_container, image_data, is_existing))
        image_item_layout.addWidget(remove_button)

        self.image_layout.addWidget(image_item_container)

    #
    # Remove an image from the image container list
    #
    def remove_image(self, container, image_data, is_existing):
        self.image_layout.removeWidget(container)
        container.deleteLater()

        if is_existing:
            self.existing_images.remove(image_data)
        else:
            self.image_paths.remove(image_data)
    

    def toggle_filter_section(self):
        """Toggle the visibility of the filter section when the filter button is clicked."""
        self.filter_section.setVisible(not self.filter_section.isVisible())
        
        # Update button text based on filter visibility
        if self.filter_section.isVisible():
            self.filter_button.setText("Hide Filters")
        else:
            self.filter_button.setText("Show Filters")

    def save_changes(self, dialog, columns, entries, item_data, message_labels):
        # Clear previous error messages
        for label in message_labels.values():
            label.setText("")
            
        validation_passed = True
        new_data = {}
        original_id = item_data[0]
        
        # Define validation types for each field
        validation_types = {
            'id': 'text',
            'name': 'text',
            'brand': 'alphanumeric_space',
            'category': 'alphanumeric_space',
            'description': 'text',
            'price': 'float',
            'quantity': 'int'
        }
        
        # First, validate all inputs
        for col in columns:
            col_lower = col.lower()
            value = entries[col].text().strip()
            
            # Required fields check - ID, Name, Price, Quantity are essential
            is_required = col_lower in ['id', 'name', 'price', 'quantity']
            if is_required and not value:
                validation_passed = False
                message_labels[col].setText(f"{col} is required")
                continue
            
            # Skip validation for empty non-required fields
            if not is_required and not value:
                continue
            
            # Get validation type for this field
            validation_type = validation_types.get(col_lower, 'text')
            
            # Perform validation based on field type
            valid = True
            error_msg = ""
            
            if validation_type == 'alphanumeric':
                if not value.isalnum():
                    valid = False
                    error_msg = f"{col} must contain only letters and numbers"
            elif validation_type == 'alphanumeric_space':
                if not all(c.isalnum() or c.isspace() for c in value):
                    valid = False
                    error_msg = f"{col} must contain only letters, numbers and spaces"
            elif validation_type == 'int':
                try:
                    int(value)
                except ValueError:
                    valid = False
                    error_msg = f"{col} must be a whole number"
            elif validation_type == 'float':
                try:
                    float(value)
                    # Check for proper decimal format
                    if '.' in value:
                        integer_part, decimal_part = value.split('.')
                        if not integer_part.isdigit() or not decimal_part.isdigit():
                            valid = False
                            error_msg = f"{col} must be a number with valid decimal"
                except ValueError:
                    valid = False
                    error_msg = f"{col} must be a valid number"
            
            if not valid:
                validation_passed = False
                message_labels[col].setText(error_msg)
            else:
                new_data[col] = value
        
        if not validation_passed:
            return
        
        # Check if trying to change ID to an existing one (except itself)
        new_id = new_data.get('id')
        if new_id and new_id != original_id:
            all_items = self.inventory_system.get_all_items()
            if new_id in all_items['id'].values:
                message_labels['id'].setText("This ID already exists. Please choose a different ID.")
                return
        
        success = self.inventory_system.update_item(original_id, new_data)
        if not success:
            QMessageBox.critical(self, "Error", "Failed to update the product.")
            
        # Update the images in the database
        try:
            # Remove deleted images
            current_images = self.inventory_system.get_images_for_product(original_id)
            for image_data in current_images:
                if image_data not in self.existing_images:
                    self.inventory_system.remove_image(original_id, image_data)

            # Add new images
            for image_path in self.image_paths:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                    self.inventory_system.add_image_to_product(original_id, image_data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update images: {str(e)}")
            return

        # Close the dialog and refresh the table
        dialog.accept()
        self.on_search()