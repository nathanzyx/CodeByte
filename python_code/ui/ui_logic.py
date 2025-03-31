import re
from PyQt6.QtWidgets import QMessageBox, QTextEdit, QLineEdit

class UILogic:
    def __init__(self, inventory_system):
        self.inventory_system = inventory_system
        self.patterns = {
            'string': r'^[a-zA-Z0-9\s]+$',  # Allow a-z, A-Z, 0-9
            'int': r'^[+-]?\d+$',  # Allow + or -, and 0-9
            'float': r'^[+-]?\d+\.\d+$'  # Allow + or -, 0-9, and period "."
        }

    def get_inventory_data(self):
        # This method doesn't need changes
        self.inventory_system.cursor.execute(f"PRAGMA table_info({self.inventory_system.items_table})")
        columns = [column[1] for column in self.inventory_system.cursor.fetchall()]
        query = f"SELECT {', '.join(columns)} FROM {self.inventory_system.items_table}"
        self.inventory_system.cursor.execute(query)
        records = self.inventory_system.cursor.fetchall()
        return columns, records

    def get_add_item_specs(self, window):
        # This method needs to return the same structure but doesn't need internal changes
        entries = {}
        message_labels = {}
        self.inventory_system.cursor.execute(f"SELECT field_name, entry_type, validation_type, required FROM {self.inventory_system.fields_table}")
        fields = self.inventory_system.cursor.fetchall()
        prod_specs = {}
        for field_name, entry_type, validation_type, required in fields:
            # Debug the required value
            print(f"Field '{field_name}' from database - required value: {required}, type: {type(required)}")
            # Ensure required is properly converted to boolean (1 = True, 0 = False)
            is_required = bool(required)
            print(f"Field '{field_name}' converted required value: {is_required}")
            
            prod_specs[field_name] = {
                'type': 'text_box_s' if validation_type in ['string', 'int', 'float'] else 'text_box_l',
                'entry_type': entry_type,
                'validation': validation_type,
                'required': is_required
            }
        return entries, message_labels, prod_specs

    def validate_entries(self, entries, message_labels):
        validation_passed = True
        product_data = {}
        for label, (entry, validation_type, is_required) in entries.items():
            # Update to handle PyQt6 widgets
            if isinstance(entry, QTextEdit):
                value = entry.toPlainText()
            elif isinstance(entry, QLineEdit):
                value = entry.text()
            else:
                value = entry.text() if hasattr(entry, 'text') else entry.toPlainText()
                
            if not self.validate_input(value, validation_type, is_required, label, message_labels):
                validation_passed = False
            else:
                product_data[label] = value
        return validation_passed, product_data

    # The get_add_field_specs method is not needed for PyQt6 as it will be implemented differently
    # in the ManageFieldsView class

    def get_existing_fields(self):
        # This method doesn't need changes
        self.inventory_system.cursor.execute(f"SELECT field_name FROM {self.inventory_system.fields_table}")
        fields = [row[0] for row in self.inventory_system.cursor.fetchall()]
        return fields
        
    def get_field_details(self, field_name):
        """
        Get details about a specific field including validation type and required status
        """
        try:
            # Query the database for field details
            self.inventory_system.cursor.execute(
                f"SELECT entry_type, validation_type, required FROM {self.inventory_system.fields_table} WHERE field_name = ?", 
                (field_name,)
            )
            result = self.inventory_system.cursor.fetchone()
            
            if result:
                return {
                    'entry_type': result[0],
                    'validation_type': result[1],
                    'required': bool(result[2])  # Convert to boolean
                }
            else:
                # Return default values if field not found in metadata
                return {'validation_type': 'string', 'required': False}
                
        except Exception as e:
            print(f"Error getting field details: {str(e)}")
            # Return default values on error
            return {'validation_type': 'string', 'required': False}

    def validate_field_specs(self, field_name, entry_type_value, validation_type_value, required_value):
        if " " in field_name:
            QMessageBox.critical(None, "Error", "Name cannot contain spaces.")
            return False
        if entry_type_value not in ["small_box", "large_box"]:
            QMessageBox.critical(None, "Error", "Entry type must be 'small_box', or 'large_box'.")
            return False
        if validation_type_value not in ["string", "int", "float"]:
            QMessageBox.critical(None, "Error", "Validation type must be 'string', 'int', or 'float'.")
            return False
        if required_value not in ["0", "1"]:
            QMessageBox.critical(None, "Error", "Required must be 0 or 1.")
            return False
        return True
        
    def add_field_to_database(self, field_name, entry_type, validation_type, required):
        # Make sure required is passed as an integer
        required_int = int(required) if isinstance(required, str) else required
        
        # Validate field specifications - use required_int instead of required
        if not self.validate_field_specs(field_name, entry_type, validation_type, str(required_int)):
            return False
            
        try:
            # Add the field to the database - pass required_int
            self.inventory_system.add_to_fields_table(field_name, entry_type, validation_type, required_int)
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to add field: {str(e)}")
            print(f"Error adding field: {str(e)}")
            return False

    def validate_input(self, value, validation_type, is_required, label, message_labels):
        # Required check is now handled in add_item_submit
        if not value.strip():
            return not is_required  # Return True only if field is not required
            
        if validation_type == 'string' and not re.match(self.patterns['string'], value):
            message_labels[label].setText(f"{label} contains invalid characters.")
            return False
        if validation_type == 'int' and not re.match(self.patterns['int'], value):
            message_labels[label].setText(f"{label} must be an integer.")
            return False
        if validation_type == 'float' and not re.match(self.patterns['float'], value):
            message_labels[label].setText(f"{label} must be a float (contain decimal point) ex. 0.00.")
            return False
        return True