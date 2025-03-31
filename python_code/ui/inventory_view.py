from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
                            QPushButton, QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QMessageBox, QDialog, QFormLayout, QListWidget, 
                            QListWidgetItem, QCheckBox, QScrollArea, QComboBox, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QColor
import pandas as pd
import re

class InventoryView(QMainWindow):
    def __init__(self, parent, inventory_system):
        super().__init__(parent)
        self.inventory_system = inventory_system
        self.selected_fields = set()
        self.setup_ui()

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
        
        # Create a grid layout for field checkboxes (removed Select All checkbox)
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
        
        # Remove the Apply Filters button since filtering happens automatically
        # when checkboxes are toggled
        
        main_layout.addWidget(self.filter_section)

        # Table section
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
        self.table.setStyleSheet("""
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
        
        # Update the table
        self.on_search()

    def on_search(self):
        """Search inventory based on query and selected fields"""
        query = self.search_entry.text()
        
        # Get all items first
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
                # If no fields selected, don't show any results
                df = df.iloc[0:0]  # Empty DataFrame with same columns
                
        self.update_table(df)

    def on_table_double_click(self, index):
        row = index.row()
        # Get all column headers
        headers = []
        for col in range(self.table.columnCount()):
            headers.append(self.table.horizontalHeaderItem(col).text())
            
        # Get data for all columns
        item_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
        self.modify_item(item_data, headers)

    def modify_item(self, item_data, columns):
        if not item_data:
            return

        mod_dialog = QDialog(self)
        mod_dialog.setWindowTitle("Modify Product")
        mod_dialog.resize(500, 500)
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

        dialog_layout = QVBoxLayout(mod_dialog)
        dialog_layout.setContentsMargins(20, 20, 20, 20)
        dialog_layout.setSpacing(15)
        
        title = QLabel("Edit Product Details")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        dialog_layout.addWidget(title)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        entries = {}

        for idx, col in enumerate(columns):
            label = QLabel(col.capitalize())
            label.setFont(QFont("Segoe UI", 12))

            entry = QLineEdit()
            entry.setFont(QFont("Segoe UI", 12))
            entry.setText(str(item_data[idx]))

            form_layout.addRow(label, entry)
            entries[col] = entry

        dialog_layout.addLayout(form_layout)

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
        save_btn.clicked.connect(lambda: self.save_changes(mod_dialog, columns, entries, item_data))
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        dialog_layout.addWidget(button_container)
        mod_dialog.exec()

    def toggle_filter_section(self):
        """Toggle the visibility of the filter section when the filter button is clicked."""
        self.filter_section.setVisible(not self.filter_section.isVisible())
        
        # Update button text based on filter visibility
        if self.filter_section.isVisible():
            self.filter_button.setText("Hide Filters")
        else:
            self.filter_button.setText("Show Filters")

    def save_changes(self, dialog, columns, entries, item_data):
        new_data = {col: entries[col].text() for col in columns}
        original_id = item_data[0]
        new_id = new_data['id']
        
        # Check if trying to change ID to an existing one (except itself)
        if new_id != original_id:
            all_items = self.inventory_system.get_all_items()
            if new_id in all_items['id'].values:
                QMessageBox.critical(self, "Error", "This ID already exists. Please choose a different ID.")
                return
    
        success = self.inventory_system.update_item(original_id, new_data)
        if success:
            dialog.accept()
            self.on_search()
        else:
            QMessageBox.critical(self, "Error", "Failed to update the product.")

    def display_all_items(self):
        """Display all items in the inventory"""
        # Get all items as a DataFrame
        items_df = self.inventory_system.get_all_items()
        
        # Update the table with all items
        self.update_table(items_df)
        
    def update_table(self, df):
        """Update the table with data from a DataFrame"""
        # Clear the current table
        self.table.setRowCount(0)
        
        if df.empty:
            return
            
        # Set up table columns
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        
        # Add items to table
        for row_idx, (_, row_data) in enumerate(df.iterrows()):
            self.table.insertRow(row_idx)
            for col_idx, field in enumerate(df.columns):
                value = row_data[field]
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        # Set column resize mode based on number of columns
        if len(df.columns) <= 7:
            # If 7 or fewer columns, stretch to fill the width
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        else:
            # If more than 7 columns, use fixed width with scrollbar
            for i in range(len(df.columns)):
                self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)