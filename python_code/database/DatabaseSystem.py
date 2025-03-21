import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Frame
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
        
        self.username = "123"
        self.password = "123"
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
        
        # Convert the required fields from True/False to 1/0
        required_int = 0
        if required:
            required_int = 1
            
        try:
            # Insert field and its info to fields table
            self.cursor.execute("INSERT INTO fields VALUES (?, ?, ?, ?)", (field_name, entry_type, validation_type, required_int))
            self.conn.commit()
            
            # Check if the column already exists in the products table
            self.cursor.execute(f"PRAGMA table_info({self.items_table})")
            existing_columns = [column[1] for column in self.cursor.fetchall()]

            # If the column doesn't exist, add it to the products table
            if field_name not in existing_columns:
                sql_type = {"string": "TEXT", "int": "INTEGER", "float": "REAL"}[validation_type]
                self.cursor.execute(f"ALTER TABLE {self.items_table} ADD COLUMN {field_name} {sql_type}")
                self.conn.commit()
            
            print(f"Field '{field_name}' added successfully!")
            return True
        except sqlite3.IntegrityError:
            print(f"Field '{field_name}' already exists.")
        return False

    
    
    #
    #   This function removes a field from the fields table
    #   When a field is removed, the user will no longer be prompted to enter that field when adding an item to inventory
    #
    def remove_to_fields_table(self, field_name):
        # This function adds field to the fields table
        self.cursor.execute(f"DELETE FROM {self.fields_table} WHERE field_name = ?", (field_name,))
        self.conn.commit()
        print(f"Field '{field_name}' removed successfully!")
    
    

    
    #
    #   This function:
    #       - Retrieves product data from the UI function display_add_item()
    #       - Inputs the products data into its categories in the database
    #
    def add_item_to_database(self, product_data):
    
        # Fetch field names from the database (excluding primary keys or auto-generated fields if needed)
        self.cursor.execute(f"SELECT field_name FROM {self.fields_table}")
        fields = [row[0] for row in self.cursor.fetchall()]

        # Ensure all required fields are present
        # Iterates through field in fields, then checks if field is not in product data
        missing_fields = [field for field in fields if field not in product_data]
        if missing_fields:
            print(f"Missing fields: {missing_fields}")
            return False

        # Prepare dynamic SQL query
        placeholders = ", ".join(["?" for _ in fields])
        field_names = ", ".join(fields)
        values = tuple(product_data[field] for field in fields)

        # Add items to database
        self.cursor.execute(f"INSERT INTO {self.items_table} ({field_names}) VALUES ({placeholders})", values)
        self.conn.commit()
        
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
            return True
        except Exception as e:
            print(f"Error updating item: {e}")
            return False
          
    #
    #   This function is temporary for testing, it simply clears the 'products' table of the database
    #   You can also just delete the database file for a fresh start
    #
    def clear_database(self):
        # Show confirmation dialog
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the database? This action cannot be undone."):
            self.cursor.execute(f"DELETE FROM {self.items_table}")
            self.conn.commit()
            messagebox.showinfo("Success", "Database cleared successfully.")
        else:
            messagebox.showinfo("Cancelled", "Database clear operation cancelled.")
