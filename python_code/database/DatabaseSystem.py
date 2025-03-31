import pandas as pd
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QWidget
from datetime import datetime
from ui import *
import sqlite3
import os

#   InventorySystem Class
#
#   This class is for handling operations of a database
#

class DatabaseSystem:
    def __init__(self, name: str, file: str):
        # Define name of databse instance
        self.name = name
        
        self.ui = None  # Initialize UI later
        
        # Define SQLite database file name and table names for reference
        self.db = file
        self.items_table = "products"
        self.fields_table = "fields"
        
        # We get the log file in append mode
        self.log_file = self.getLogFile(name, ".txt")
        
        self.username = "admin"
        self.password = "321"
        self.logged_in = False
        
        # Create/Connect SQLite3 Database "products" (and table)
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        
        # Check if main table 'product' exists
        products_exists = self.table_exists(self.items_table)
        # If the 'products' table does not yet exist, we create it and a new table for fields
        if not products_exists:
            self.create_fields_table()
            self.create_products_table()
    
    #
    #   This function returns the log file for the database in append mode
    #       - Will create a new file if it does not exist
    #
    def getLogFile(self, name: str, type: str):
        log_file_path = f"{name}{type}"
        # Ensure file exists before opening
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w') as file:
                file.write("")  # Create an empty file
        
        # Open file in append mode and return the file object
        return open(log_file_path, 'a')
    
    #
    #   This function writes a message to the log file
    # 
    def log_message(self, message: str):
        # Create the time of the message
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        
        self.log_file.write(f"{timestamp} {message}\n")
        self.log_file.flush()
            
    
    
    def set_ui(self, ui):
        self.ui = ui
        
    #
    #   This function returns a boolean value for whether a given table exists in the database
    #
    def table_exists(self, table_name):
        # Check if the 'products' table exists. Return True if it does, False otherwise.
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        table_exists = self.cursor.fetchone()
        return bool(table_exists)  # True if table exists, False otherwise
    
    
    
    #
    # Creates the default table for fields (only called if products table does not exist)
    #
    def create_fields_table(self):
        # Creates a new table (if it doesn't already exist) for input fields
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.fields_table} (
                field_name TEXT PRIMARY KEY,
                entry_type TEXT CHECK(entry_type IN ('small_box', 'large_box')),
                validation_type TEXT CHECK(validation_type IN ('string', 'int', 'float')),
                required INTEGER CHECK(required IN (0, 1))
            )
        ''')
        self.conn.commit()
        
        # Define the default input fields
        default_fields = [
            ('id', 'small_box', 'string', 1),
            ('name', 'small_box', 'string', 1),
            ('quantity', 'small_box', 'int', 1),
            ('price', 'small_box', 'float', 1),
            ('category', 'small_box', 'string', 1),
            ('brand', 'small_box', 'string', 1),
            ('description', 'large_box', 'string', 0)
        ]
        # Insert the default input fields into the database's field table
        self.cursor.executemany(f"INSERT OR IGNORE INTO {self.fields_table} VALUES (?, ?, ?, ?)", default_fields)
        self.conn.commit()
    
    
    
    #
    #   This function creates the main table of the database
    #   The products table will hold all the inventory
    #   The products table is created with each column corresponding to each field from the field table
    #
    def create_products_table(self):
        # Gets all field names from fields table (to get columns for main table)
        self.cursor.execute(f"SELECT field_name, validation_type FROM {self.fields_table}")
        fields = self.cursor.fetchall()

        # Associate validation type to fields
        column_definitions = []
        for field, field_type in fields:
            sql_type = {"string": "TEXT", "int": "INTEGER", "float": "REAL"}[field_type]
            column_definitions.append(f"{field} {sql_type}")

        # Create table with the new fields
        sql = f"CREATE TABLE IF NOT EXISTS {self.items_table} ({', '.join(column_definitions)})"
        self.cursor.execute(sql)
        self.conn.commit()
        
        
        
    #
    #   This function adds a new field into the fields table
    #   When the user adds a product to the inventory, they are prompted to fill out each field
    #   By adding fields, we allow the user to input more information when adding a product
    #
    def add_to_fields_table(self, field_name, entry_type, validation_type, required):
        
        # Convert the required parameter to integer (0 or 1)
        # This handles both string values ("0"/"1") and integer values (0/1)
        if isinstance(required, str):
            required_int = 1 if required == "1" else 0
        else:
            required_int = 1 if required else 0
            
        try:
            # Check if field already exists in fields table
            self.cursor.execute(f"SELECT COUNT(*) FROM {self.fields_table} WHERE field_name=?", (field_name,))
            if self.cursor.fetchone()[0] > 0:
                raise ValueError(f"Field '{field_name}' already exists in fields table")
                
            # Insert field and its info to fields table
            self.cursor.execute(f"INSERT INTO {self.fields_table} VALUES (?, ?, ?, ?)", 
                               (field_name, entry_type, validation_type, required_int))
            self.conn.commit()
            
            # Check if the column already exists in the products table
            self.cursor.execute(f"PRAGMA table_info({self.items_table})")
            existing_columns = [column[1] for column in self.cursor.fetchall()]
        
            # If the column doesn't exist, add it to the products table
            if field_name not in existing_columns:
                sql_type = {"string": "TEXT", "int": "INTEGER", "float": "REAL"}[validation_type]
                self.cursor.execute(f"ALTER TABLE {self.items_table} ADD COLUMN {field_name} {sql_type}")
                self.conn.commit()
            else:
                # If column exists but not in fields table, we have a sync issue
                raise ValueError(f"Column '{field_name}' already exists in products table but was not in fields table")
            
            # LOG MESSAGE
            self.log_message(f"Field Added: field_name:{str(field_name)}, entry_type:{str(entry_type)}, validation_type:{str(validation_type)}, required:{str(required_int)}")
            return True
        except sqlite3.IntegrityError as e:
            # LOG MESSAGE
            self.log_message(f"ERROR: Field Added Attempted: field_name:{str(field_name)}, entry_type:{str(entry_type)}, validation_type:{str(validation_type)}, required:{str(required_int)}")
            raise ValueError(f"Database integrity error: {str(e)}")
        except Exception as e:
            self.log_message(f"ERROR: Field Added Attempted: field_name:{str(field_name)}, entry_type:{str(entry_type)}, validation_type:{str(validation_type)}, required:{str(required_int)}")
            raise e
        return False

    
    
    #
    #   This function removes a field from the fields table
    #   When a field is removed, the user will no longer be prompted to enter that field when adding an item to inventory
    #
    def remove_to_fields_table(self, field_name):
        # This function adds field to the fields table
        self.cursor.execute(f"DELETE FROM {self.fields_table} WHERE field_name = ?", (field_name,))
        self.conn.commit()
        # LOG MESSAGE
        self.log_message(f"Field Removed: field_name:{str(field_name)}")
    
    

    
    #
    #   This function:
    #       - Retrieves product data from the UI function display_add_item()
    #       - Inputs the products data into its categories in the database
    #
    def add_item_to_database(self, product_data):
        # Fetch field names and required status from the database
        self.cursor.execute(f"SELECT field_name, required FROM {self.fields_table}")
        field_info = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        print(f"Field info from database: {field_info}")
        
        # Get all field names
        fields = list(field_info.keys())
        
        # Check for missing fields
        missing_fields = [field for field in fields if field not in product_data]
        if missing_fields:
            print(f"Missing fields: {missing_fields}")
            return False
        
        # Check for required fields with empty values
        empty_required_fields = [field for field, required in field_info.items() 
                                if required == 1 and field in product_data and not product_data[field]]
        
        if empty_required_fields:
            print(f"Empty required fields: {empty_required_fields}")
            return False
    
        # Prepare dynamic SQL query
        placeholders = ", ".join(["?" for _ in fields])
        field_names = ", ".join(fields)
        values = tuple(product_data.get(field, "") for field in fields)
    
        # Add items to database
        self.cursor.execute(f"INSERT INTO {self.items_table} ({field_names}) VALUES ({placeholders})", values)
        self.conn.commit()
        
        # LOG MESSAGE
        self.log_message(f"Item Added: field_name:{str(product_data)}")
        return True
    
    
    
    #
    #   This function:
    #       - Retreives the ID and count of the item to be removed
    #       - Ensures item exists, if so decreases quantity by requested amount
    #       - Ensures the user cannot remove more of an item than currently exists
    #
    def remove_item_from_database(self, item_id, item_count):
        # Directly select the quantity column
        self.cursor.execute(f"SELECT quantity FROM {self.items_table} WHERE id=?", (item_id,))
        item = self.cursor.fetchone()

        # If item is not found
        if not item:
            raise ValueError("Item not found.")
        
        # 'quantity' will be at index 0
        current_quantity = item[0]
        
        item_count = int(item_count)

        # Check if the number of items to remove exceeds the available quantity
        if item_count > current_quantity:
            raise ValueError("Cannot remove more items than are available in the inventory.")

        # Decrease the item count by the specified amount
        new_quantity = current_quantity - item_count
        self.cursor.execute(f"UPDATE {self.items_table} SET quantity=? WHERE id=?", (new_quantity, item_id))
        self.conn.commit()
        
        self.log_message(f"Item Removed: id:{str(item_id)}, count:{str(item_count)}")
        
    
    def get_all_items(self):
        # Execute query to select all records from the products table
        self.cursor.execute(f"SELECT * FROM {self.items_table}")
        items = self.cursor.fetchall()
        
        # Get column names using cursor description
        columns = [desc[0] for desc in self.cursor.description]
        
        return pd.DataFrame(items, columns=columns)

    #
    #   This function searches the database for items that match the query
    #
    def search_items(self, fields, query):
        # If no fields are selected, return an empty DataFrame (wiht the field columns)
        if not fields:
            # We select all items from the database
            self.cursor.execute(f"SELECT * FROM {self.items_table}")
            # Then we take only the columns
            columns = [desc[0] for desc in self.cursor.description]
            return pd.DataFrame(columns=columns)

        # Make List for conditions and parameters
        conditions = []
        params = []
        # Iterate over each column name (field)
        for field in fields:
            conditions.append(f"{field} LIKE ?")
            # '%' is a wildcard, and means we can match any occurence of the query (ex. "23" in "1234")
            params.append(f"%{query}%")
            
        # Make final SQL query with all conditions
        sql = (f"SELECT * FROM {self.items_table} WHERE " + " OR ".join(conditions))
        
        # Execute SQL query and get results
        self.cursor.execute(sql, params)
        search_results = self.cursor.fetchall()
        
        # Return the results as a DataFrame, with the search result items, and the extracted column names
        return pd.DataFrame(search_results, columns=[desc[0] for desc in self.cursor.description])
        
    def update_item(self, item_id, new_data):
        # Create the SET query dynamically (e.g. "name=?, price=?, ...")
        set_clause = ", ".join([f"{column}=?" for column in new_data])
        # extract the new item data from the parameter
        values = list(new_data.values())
        # add the values
        values.append(item_id)
        
        try:
            # Execute update statement
            sql = f"UPDATE {self.items_table} SET {set_clause} WHERE id=?"
            self.cursor.execute(sql, values)
            self.conn.commit()
            
            # LOG MESSAGE
            self.log_message(f"Item Modified: id:{str(item_id)}, new_data:{str(new_data)}")
            
            return True
        except Exception as e:
            print(f"Error updating item: {e}")
            return False
          
    #
    #   This function is temporary for testing, it simply clears the 'products' table of the database
    #   You can also just delete the database file for a fresh start
    #
    def clear_database(self):
        # Show confirmation dialog using PyQt6
        confirm = QMessageBox.question(
            None, 
            "Confirm", 
            "Are you sure you want to clear the database? This will remove ALL items and custom fields. This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Drop the products table completely instead of just deleting rows
                self.cursor.execute(f"DROP TABLE IF EXISTS {self.items_table}")
                
                # Clear custom fields (but keep the built-in fields)
                built_in_fields = ["brand", "category", "description", "id", "name", "price", "quantity"]
                placeholders = ", ".join(["?" for _ in built_in_fields])
                self.cursor.execute(f"DELETE FROM {self.fields_table} WHERE field_name NOT IN ({placeholders})", built_in_fields)
                
                # Recreate the products table with the remaining fields
                self.create_products_table()
                
                self.conn.commit()
                QMessageBox.information(None, "Success", "Database cleared successfully. All items and custom fields have been removed.")
                # LOG MESSAGE
                self.log_message("Database Cleared! (Items and custom fields)")
                return True
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to clear database: {str(e)}")
                print(f"Error clearing database: {str(e)}")
                return False
        return False


# Make sure this method is properly indented to be part of the DatabaseSystem class
def remove_field_from_database(self, field_name):
    """Remove a field from the database"""
    try:
        # First, check if the field exists
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.fields_table} WHERE field_name=?", (field_name,))
        if self.cursor.fetchone()[0] == 0:
            raise ValueError(f"Field '{field_name}' does not exist")
            
        # Remove the field from the fields table
        self.cursor.execute(f"DELETE FROM {self.fields_table} WHERE field_name=?", (field_name,))
        
        # SQLite doesn't support DROP COLUMN directly, so we need to:
        # 1. Get all columns except the one to remove
        self.cursor.execute(f"PRAGMA table_info({self.items_table})")
        columns = [column[1] for column in self.cursor.fetchall() if column[1] != field_name]
        
        # 2. Create a new table without the column
        columns_str = ", ".join(columns)
        self.cursor.execute(f"CREATE TABLE temp_table AS SELECT {columns_str} FROM {self.items_table}")
        
        # 3. Drop the old table
        self.cursor.execute(f"DROP TABLE {self.items_table}")
        
        # 4. Rename the new table
        self.cursor.execute(f"ALTER TABLE temp_table RENAME TO {self.items_table}")
        
        self.conn.commit()
        self.log_message(f"Field Removed: field_name:{str(field_name)}")
        return True
    except Exception as e:
        self.log_message(f"ERROR: Field Removal Attempted: field_name:{str(field_name)}")
        raise e

# Add a method to get field information including required status
def get_field_info(self, field_name=None):
    """Get information about fields including their required status"""
    try:
        if field_name:
            self.cursor.execute(f"SELECT field_name, entry_type, validation_type, required FROM {self.fields_table} WHERE field_name=?", (field_name,))
            result = self.cursor.fetchone()
            if result:
                return {
                    'field_name': result[0],
                    'entry_type': result[1],
                    'validation_type': result[2],
                    'required': bool(result[3])  # Convert 0/1 to False/True
                }
            return None
        else:
            self.cursor.execute(f"SELECT field_name, entry_type, validation_type, required FROM {self.fields_table}")
            results = self.cursor.fetchall()
            return [{
                'field_name': row[0],
                'entry_type': row[1],
                'validation_type': row[2],
                'required': bool(row[3])  # Convert 0/1 to False/True
            } for row in results]
    except Exception as e:
        print(f"Error getting field info: {str(e)}")
        return [] if field_name is None else None
