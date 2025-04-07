import pandas as pd
import json
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QWidget, QLineEdit
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
        self.images_table = "images"
        self.fields_table = "fields"
        self.login_table = "login"
        
        # We get the log file in append mode
        self.log_file = self.getLogFile(name, ".txt")
        
        self.username = ""
        self.password = ""
        self.logged_in = False
        
        # Create/Connect SQLite3 Database "products" (and table)
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        
        # Check if main table 'product' exists & Create 'products table if it does not exist'
        products_exists = self.table_exists(self.items_table)
        if not products_exists:
            self.create_fields_table()
            self.create_products_table()
            self.create_images_table()
            self.create_login_table()
    
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
                entry_type TEXT CHECK(entry_type IN ('small_box', 'large_box', 'image_box')),
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
            ('description', 'large_box', 'string', 0),
            # ('images', 'image_box', 'string', 0)
        ]
        # Insert the default input fields into the database's field table
        self.cursor.executemany(f"INSERT OR IGNORE INTO {self.fields_table} VALUES (?, ?, ?, ?)", default_fields)
        self.conn.commit()
    
    
    #
    #   This function creates the login table which holds:
    #       - username
    #       - password
    #       - login required for performing database operations
    #
    def create_login_table(self):
        # Create the login table if it doesn't already exist
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.login_table} (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                requires_login INTEGER CHECK(requires_login IN (0, 1)) NOT NULL
            )
        ''')
        self.conn.commit()
        
        # Insert default login credentials if the table is empty
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.login_table}")
        if self.cursor.fetchone()[0] == 0:
            default_login = ("", "", 0)  # Default username, password, and requires_login flag
            self.cursor.execute(f"INSERT INTO {self.login_table} VALUES (?, ?, ?)", default_login)
            self.conn.commit()
    
    
    #
    #   Returns whether logging in is required to perform database actions
    #
    def login_required(self):
        try:
            # Get login required value
            self.cursor.execute(f"SELECT requires_login FROM {self.login_table} LIMIT 1")
            result = self.cursor.fetchone()

            # Return true if the result is valid and login is set to required
            if result and result[0] == 1:
                return True
            return False
        except Exception as e:
            self.log_message(f"Error checking login requirement: {str(e)}")
            return False
    
    #
    #   Returns whether account exists
    #
    def account_exists(self):
        try:
            # Query the login table for any non-empty username and password
            self.cursor.execute(f"SELECT username, password FROM {self.login_table} WHERE username != '' AND password != '' LIMIT 1")
            result = self.cursor.fetchone()

            # Return True if a valid account exists
            return bool(result)
        except Exception as e:
            self.log_message(f"Error checking account existence: {str(e)}")
            return False
        # try:
        #     # Query the login table for any non-empty username and password
        #     self.cursor.execute(f"SELECT username, password FROM {self.login_table} LIMIT 1")
        #     result = self.cursor.fetchone()

        #     # Check if username and password are not empty
        #     if result and result[0] and result[1]:
        #         return True
        #     return False
        # except Exception as e:
        #     self.log_message(f"Error checking account existence: {str(e)}")
        #     return False
    
    #
    #   Modifies account credentials if the old credentials match
    #
    def set_account_credentials(self, newUsername, newPassword, login_required):
        try:
            # Get password from the login table
            self.cursor.execute(f"SELECT password FROM {self.login_table} WHERE username=?", (self.username,))
            result = self.cursor.fetchone()

            # If username exists and password matches the usernames stored password
            if not result or result[0] != self.password:
                self.log_message("Failed to update credentials: Invalid old username or password.")
                return False

            # Update account credentials with the new values
            self.cursor.execute(f'''
                UPDATE {self.login_table}
                SET username=?, password=?, requires_login=?
                WHERE username=?
            ''', (newUsername, newPassword, login_required, self.username))
            self.conn.commit()

            self.log_message(f"Account credentials updated successfully: New username '{newUsername}'.")
            return True
        except Exception as e:
            self.log_message(f"Error updating account credentials: {str(e)}")
            return False
        
        
    #
    #   Attempts to log in the user using credentials
    #
    def login(self, username, password):
        try:
            # Query the login table for the provided username
            self.cursor.execute(f"SELECT password, requires_login FROM {self.login_table} WHERE username=?", (username,))
            result = self.cursor.fetchone()

            # If no user is found or login is not required
            if not result:
                self.log_message(f"Login failed: Username '{username}' not found.")
                return False
            # if result[1] == 0:  # requires_login is False
            #     self.log_message("Login not required, access granted.")
            #     return True

            # Check if the provided password matches the stored password
            stored_password = result[0]
            if password == stored_password:
                self.logged_in = True
                self.log_message(f"LOGIN: Username '{username}'.")
                
                # set database username
                self.username = username
                self.password = password
                
                return True
            else:
                self.log_message(f"Login failed: Incorrect password for username '{username}'.")
                return False
        except Exception as e:
            self.log_message(f"Login error: {str(e)}")
            return False
    
    
    
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
           
        # Add image column to the database 
        # column_definitions.append("images TEXT")

        # Create table with the new fields
        sql = f"CREATE TABLE IF NOT EXISTS {self.items_table} ({', '.join(column_definitions)})"
        self.cursor.execute(sql)
        self.conn.commit()
        
    def create_images_table(self):
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.images_table} (
                    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    image_data BLOB NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES {self.items_table}(id) ON DELETE CASCADE
                )
            """)
            self.conn.commit()
            self.log_message("Images table created successfully.")
        except Exception as e:
            self.log_message(f"Error creating images table: {str(e)}")
            raise e
        
        
        
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
        print(f"Product info from database: {product_data}")
        
        # Get all field names (except form images)
        # fields = list(field_info.keys())
        fields = [field for field in field_info.keys() if field != "images"]
        
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
        
        try:
            # Insert the product data into the products table
            self.cursor.execute(f"INSERT INTO {self.items_table} ({field_names}) VALUES ({placeholders})", values)
            product_id = self.cursor.lastrowid  # Get the ID of the newly inserted product

            # Insert image data into the images table
            if "images" in product_data and product_data["images"]:
                for image_path in product_data["images"]:
                    try:
                        with open(image_path, "rb") as image_file:
                            image_data = image_file.read()  # Read the image as binary data
                            self.cursor.execute(f"INSERT INTO {self.images_table} (product_id, image_data) VALUES (?, ?)", (product_id, image_data))
                    except Exception as e:
                        self.log_message(f"Error reading image file '{image_path}': {str(e)}")
                        print(f"Error reading image file '{image_path}': {str(e)}")

            self.conn.commit()
            
            # LOG MESSAGE
            self.log_message(f"Item Added: {product_data}")
            return True
        except Exception as e:
            self.log_message(f"Error adding item to database: {str(e)}")
            print(f"Error adding item to database: {str(e)}")
            return False
    
        # # Add items to database
        # self.cursor.execute(f"INSERT INTO {self.items_table} ({field_names}) VALUES ({placeholders})", values)
        # self.conn.commit()
        
        # # LOG MESSAGE
        # self.log_message(f"Item Added: field_name:{str(product_data)}")
        # return True
    
    
    
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
        
    #
    #   Returns all images for a product specified by its ID in the form of a list of binary data
    #
    def get_images_for_product(self, product_id):
        try:
            self.cursor.execute(f"SELECT image_data FROM {self.images_table} WHERE product_id = ?", (product_id,))
            images = self.cursor.fetchall()
            return [image[0] for image in images]  # Return a list of binary image data
        except Exception as e:
            self.log_message(f"Error retrieving images for product_id {product_id}: {str(e)}")
            raise e
    #
    #   Removes an image from a product specified by its ID, and matching image data. Does not return status of whether the image was or wasn't found
    #
    def remove_image(self, product_id, image_data):
        try:
            self.cursor.execute(f"DELETE FROM {self.images_table} WHERE product_id = ? AND image_data = ?", (product_id, image_data))
            self.conn.commit()
            self.log_message(f"Image removed for product_id {product_id}")
        except Exception as e:
            self.log_message(f"Error removing image for product_id {product_id}: {str(e)}")
            raise e
    
    #
    #   Adds an image to a product specified by its ID
    #
    def add_image_to_product(self, product_id, image_data):
        try:
            self.cursor.execute(f"INSERT INTO {self.images_table} (product_id, image_data) VALUES (?, ?)", (product_id, image_data))
            self.conn.commit()
            self.log_message(f"Image added for product_id {product_id}")
        except Exception as e:
            self.log_message(f"Error adding image for product_id {product_id}: {str(e)}")
            raise e
        
    #
    #   Returns all items as a dataframe
    #
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
            # Check if the ID is being updated (so the linking images in the image table have their key updated)
            new_id = new_data.get("id")
            if new_id and new_id != item_id:
                # Update the product ID in the images table first
                self.cursor.execute(f"UPDATE {self.images_table} SET product_id=? WHERE product_id=?", (new_id, item_id))
            
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
    #    This function returns a dataframe of the result of the list of ids it was given
    #
    def get_products_by_id(self, ids):
        if not ids:
            # if ids are empty, returns an empty dataframe
            return pd.DataFrame(columns=[desc[0] for desc in self.cursor.description])

        try:
            # Make Placeholder
            placeholders = ", ".join(["?"] * len(ids))
            sql = f"SELECT * FROM {self.items_table} WHERE id IN ({placeholders})"
            
            self.cursor.execute(sql, ids)
            results = self.cursor.fetchall()

            # Get columns
            columns = [desc[0] for desc in self.cursor.description]

            return pd.DataFrame(results, columns=columns)
        except Exception as e:
            self.log_message(f"Error retrieving products by IDs: {str(e)}")
            raise e
        
        
    #
    #   This function is temporary for testing, it simply clears the 'products' table of the database
    #   You can also just delete the database file for a fresh start
    #
    def clear_database(self):
        # Show confirmation dialog using PyQt6
        if self.account_exists():
            password, ok = QInputDialog.getText(
                None, "Confirm Password", "Enter your password to clear the database:", QLineEdit.EchoMode.Password
            )
            if not ok:
                return False

            # Verify password
            if password != self.password:
                QMessageBox.critical(None, "Authentication Failed", "The password you entered is incorrect.")
                return False


        # Show confirmation dialog
        confirm = QMessageBox.question(
            None, "Confirm", "Are you sure you want to clear the database? This action will delete all inventory data and custom fields.",)
        
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Drop the products table completely instead of just deleting rows
                self.cursor.execute(f"DROP TABLE IF EXISTS {self.items_table}")
                self.cursor.execute(f"DROP TABLE IF EXISTS {self.images_table}")
                
                # Clear custom fields (but keep the built-in fields)
                built_in_fields = ["brand", "category", "description", "id", "name", "price", "quantity"]
                placeholders = ", ".join(["?" for _ in built_in_fields])
                self.cursor.execute(f"DELETE FROM {self.fields_table} WHERE field_name NOT IN ({placeholders})", built_in_fields)
                
                # Recreate the products table with the remaining fields
                self.create_products_table()
                self.create_images_table()
                
                self.conn.commit()
                QMessageBox.information(None, "Success", "Database cleared, all inventory data and custom fields have been deleted.")
                # LOG MESSAGE
                self.log_message("Database Cleared! (Items and custom fields)")
                return True
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to clear database: {str(e)}")
                print(f"Error clearing database: {str(e)}")
                return False
        return False

    def remove_field_from_database(self, field_name):
        try:
            # check if field exists
            self.cursor.execute(f"SELECT COUNT(*) FROM {self.fields_table} WHERE field_name=?", (field_name,))
            if self.cursor.fetchone()[0] == 0:
                raise ValueError(f"Field '{field_name}' does not exist")
                
            # Remove field from the fields table
            self.cursor.execute(f"DELETE FROM {self.fields_table} WHERE field_name=?", (field_name,))
            
            # SQLite doesn't support DROP COLUMN directly
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

    # Method to get field information including required status
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
