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
        
        # self.inventory = []
        self.ui = UI(self)
        
        # Define SQLite database file name and table names for reference
        self.db = file
        self.items_table = "products"
        self.fields_table = "fields"
        
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
        self.cursor.execute(f"SELECT field_name, validation_type FROM {self.fields_table}")
        fields = self.cursor.fetchall()

        column_definitions = []
        for field, field_type in fields:
            sql_type = {"string": "TEXT", "int": "INTEGER", "float": "REAL"}[field_type]
            column_definitions.append(f"{field} {sql_type}")

        sql = f"CREATE TABLE IF NOT EXISTS {self.items_table} ({', '.join(column_definitions)})"
        self.cursor.execute(sql)
        self.conn.commit()
    
    
    
    #
    #   Calls display function for the Options menu in the UI class
    #
    def display_options(self):
        self.ui.display_options()
        
        
        
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
    #   This function calls the UI function to display the Main Menu
    #    
    def start_ui(self):
        self.ui.display_menu()


    
    
    #
    #   This function:
    #       - Fetches all fields from the fields table
    #       - Sends those fields to a UI function so the user can fill out the fields and add the item to the inventory       
    #
    def add_item(self):
        # Fetch fields from the database
        self.cursor.execute(f"SELECT field_name, entry_type, validation_type, required FROM {self.fields_table}")
        fields = self.cursor.fetchall()

        # Build the prod_specs dictionary dynamically
        prod_specs = {}
        for field_name, entry_type, validation_type, required in fields:
            prod_specs[field_name] = {
                'type': 'text_box_s' if validation_type in ['string', 'int', 'float'] else 'text_box_l',
                'entry_type': entry_type,
                'validation': validation_type,
                'required': bool(required)
            }
            
        self.ui.display_add_item(prod_specs)
    
    

    
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
    #   This function calls a UI function which prompts the user to remove an item from the inventory
    #
    def remove_item(self):
        self.ui.display_remove_item()  
    
    
    
    
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
    
    
    
    #
    #   This function:
    #           - Retreives all column names of the table
    #           - Passes the column names to the UI display_inventory() function to display
    #
    def display_inventory(self):
        # Fetch column names from the products table
        self.cursor.execute(f"PRAGMA table_info({self.items_table})")
        columns = [column[1] for column in self.cursor.fetchall()]
        
        # Pass the columns to the UI class function to display the inventory
        self.ui.display_inventory(columns)
