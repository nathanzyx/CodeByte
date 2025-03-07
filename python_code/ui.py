import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Frame
from datetime import datetime
import re

#   UI Class
#
#   This class is for the UI of a database instance
#

class UI:
    def __init__(self, inventory_system):
        self.inventory_system = inventory_system # Create instance of inventory
        
        
    
    #
    #   This function takes all column names from the 'product' table and displays the data
    #
    def display_inventory(self, columns):
        # Create a new window for displaying inventory
        inventory_window = tk.Toplevel()
        inventory_window.title("Inventory")

        # Create treeview to display the database records as a table
        tree = ttk.Treeview(inventory_window, columns=columns, show="headings")

        # Define column headings
        for col in columns:
            tree.heading(col, text=col.capitalize())

        tree.pack(expand=True, fill="both")

        # Fetch data from SQLite database
        query = f"SELECT {', '.join(columns)} FROM {self.inventory_system.items_table}"
        self.inventory_system.cursor.execute(query)
        records = self.inventory_system.cursor.fetchall()

        # Insert inventory data into the treeview
        for record in records:
            tree.insert("", "end", values=record)
        
    
    
    #
    #   This function:
    #           - takes field inputs from field table to prompt the user to input necessary information 
    #           - Upon submitting, calls function from DatabaseSystem class to add the item to the inventory
    #
    def display_add_item(self, prod_specs):
        window = tk.Toplevel()
        window.title("Add Item")
        window.geometry("600x400")
        
        entries = {}
        message_labels = {}


        for i, (label, props) in enumerate(prod_specs.items()):
            tk.Label(window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            # Extract type of input from entry
            input_type = props['entry_type']
            
            # Determine if the input should be a single line input or multi-line
            if input_type == 'small_box':
                entry = tk.Entry(window, width=30)
            elif input_type == 'large_box':
                entry = tk.Text(window, width=30, height=5)
            
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            
            message_label = tk.Label(window, text="", fg="red", font=("consolas", 10))
            message_label.grid(row=i, column=2, padx=10, pady=5, sticky="w")
            # Store the message label for later use
            message_labels[label] = message_label
            
            # Store entry and validation type
            entries[label] = (entry, props['validation'], props.get('required', False))
        
        def add_item_submit():
            # Clear all message labels before validation
            for label in message_labels:
                message_labels[label].config(text="")
            
            # Create REGEX patterns for validation checking
            patterns = {
                'string': r'^[a-zA-Z0-9\s]+$',  # Allow a-z, A-Z, 0-9
                'int': r'^[+-]?\d+$',  # Allow + or -, and 0-9
                'float': r'^[+-]?\d+\.\d+$'  # Allow + or -, 0-9, and period "."
            }
            
            validation_passed = True
            
            for label, (entry, validation_type, is_required) in entries.items():
                value = entry.get("1.0", "end-1c") if isinstance(entry, tk.Text) else entry.get()
                    
                # If field is required and is empty
                if is_required and not value.strip():  # Strip any leading/trailing spaces
                    message_labels[label].config(text=f"{label} is required.")
                    validation_passed = False
                    continue
                # If field is NOT required and it is empty
                if not is_required and not value.strip():
                    continue
                    
                # Validation for input fields
                if validation_type == 'string':
                    if not value or not re.match(patterns['string'], value):
                        message_labels[label].config(text=f"{label} contains invalid characters.")
                        validation_passed = False
                        continue
                elif validation_type == 'int':
                    if not re.match(patterns['int'], value):
                        message_labels[label].config(text=f"{label} must be an integer.")
                        validation_passed = False
                        continue
                elif validation_type == 'float':
                    if not re.match(patterns['float'], value):
                        message_labels[label].config(text=f"{label} must be a float (contain decimal point).")
                        validation_passed = False
                        continue
            
            if not validation_passed:
                return False
            
            product_data = {label: entry.get("1.0", "end-1c") if isinstance(entry, tk.Text) else entry.get() for label, (entry, _, _) in entries.items()}

            # Pass the item with its input data to the database adding function
            self.inventory_system.add_item_to_database(product_data)
            
            # Close the form
            window.destroy()
            
            # Show success message
            messagebox.showinfo("Success", "Item added successfully.")
            return True
        
        submit_button = tk.Button(window, text="Add Item", command=add_item_submit, bg="#4CAF50", fg="white")
        submit_button.grid(row=len(prod_specs), column=1, padx=10, pady=10)

    
    
    
    
    
    
    #   REMOVE ITEM UI
    #       User Enters:
    #               - ID of Item to be Removed
    #               - Number of that Item to be Removed (int)
    def display_remove_item(self):
        window = tk.Toplevel()
        window.title("Remove Item")
        window.geometry("600x400")

        # ID to remove
        tk.Label(window, text="Enter Item ID to Remove:").pack(pady=10)
        item_id_entry = tk.Entry(window)
        item_id_entry.pack(pady=5)
        # count to remove
        tk.Label(window, text="Enter Number of Items to Remove").pack(pady=10)
        item_count_entry = tk.Entry(window)
        item_count_entry.pack(pady=5)

        # Handled item removal
        def submit():
            # Define REGEX patterns for validation checking
            patterns = {
                'string': r'^[a-zA-Z0-9\s]+$',  # Allow a-z, A-Z, 0-9
                'int': r'^[+-]?\d+$',  # Allow + or -, and 0-9
                'float': r'^[+-]?\d+\.\d+$'  # Allow + or -, 0-9, and period "."
            }
            # Get values
            item_id = item_id_entry.get().strip()
            item_count = item_count_entry.get().strip()
            
            
            if not re.match(patterns['int'], item_count):
                messagebox.showerror("Error", "Invalid Count.")
                return

            if not item_id:
                messagebox.showerror("Error", "Please enter a valid item ID.")
                return

            try:
                # Try to remove the item from the database based on the provided item ID
                self.inventory_system.remove_item_from_database(item_id, item_count)
                window.destroy()
                messagebox.showinfo("Success", f"Item with ID {item_id} removed successfully.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Submit button to execute item removal
        submit_button = tk.Button(window, text="Remove Item", command=submit, bg="#af4c4c", fg="white")
        submit_button.pack(pady=10)
        
        
        
    #   OPTIONS MENU    
    #       - Add Field (for adding product field)
    #       - Remove Field (for removing product field)
    #
    def display_options(self):
        window = tk.Toplevel()
        window.title("Manage Fields")
        window.geometry("400x300")
        
        # Function for the popup for adding a new field
        def add_field_popup():
            popup = tk.Toplevel(window)
            popup.title("Add Field")
            popup.geometry("200x500")
            popup.title("Add Field")

            # Field Name
            tk.Label(popup, text="Field Name:").pack()
            field_name_entry = tk.Entry(popup)
            field_name_entry.pack()
            # Size of field entry box
            tk.Label(popup, text="Entry Box Size:").pack()
            entry_type = tk.StringVar()
            entry_type.set("")
            # Buttons for selection
            small_box_button = tk.Button(popup, text="Small Box", command=lambda: entry_type.set("small_box"))
            small_box_button.pack(pady=5)
            large_box_button = tk.Button(popup, text="Large Box", command=lambda: entry_type.set("large_box"))
            large_box_button.pack(pady=5)
            
            # Validation Type
            tk.Label(popup, text="Input Type:").pack()
            validation_type = tk.StringVar()
            validation_type.set("")
            # Button selections for validation types
            string_box_button = tk.Button(popup, text="String", command=lambda: validation_type.set("string"))
            string_box_button.pack(pady=5)
            int_box_button = tk.Button(popup, text="Integer", command=lambda: validation_type.set("int"))
            int_box_button.pack(pady=5)
            float_box_button = tk.Button(popup, text="Decimal Value", command=lambda: validation_type.set("float"))
            float_box_button.pack(pady=5)
            
            
            # User indicates whether the field is required
            tk.Label(popup, text="Required Field:").pack()
            required = tk.StringVar()
            required.set("")
            # Buttons for required selection
            required_button = tk.Button(popup, text="Required", command=lambda: required.set("1"))
            required_button.pack(pady=5)
            not_required_button = tk.Button(popup, text="Not Required", command=lambda: required.set("0"))
            not_required_button.pack(pady=5)
            

            def submit():
                field_name = field_name_entry.get()
                entry_type_value = entry_type.get().strip()
                validation_type_value = validation_type.get().strip()
                required_value = required.get().strip()

                # Ensuring the input fields comply with wanted inputs
                if field_name.__contains__(" "):
                    messagebox.showerror("Error", "Name cannot contain spaces.")
                    return
                if entry_type_value not in ["small_box", "large_box"]:
                    messagebox.showerror("Error", "Entry type must be 'small_box', or 'large_box'.")
                    return
                if validation_type_value not in ["string", "int", "float"]:
                    messagebox.showerror("Error", "Validation type must be 'string', 'int', or 'float'.")
                    return
                if required_value not in ["0", "1"]:
                    messagebox.showerror("Error", "Required must be 0 or 1.")
                    return
                
                required_value = int(required_value)
                self.inventory_system.add_to_fields_table(field_name, entry_type_value, validation_type_value, required_value)
                popup.destroy()

            # Button for executing the new field addition
            submit_button = tk.Button(popup, text="Add Field", command=submit, bg="#4CAF50", fg="white")
            submit_button.pack()

        # This function is for field removal
        def remove_field_popup():
            popup = tk.Toplevel(window)
            popup.title("Remove Field")
            popup.geometry("300x400")

            # Fetch existing fields from the database
            self.inventory_system.cursor.execute(f"SELECT field_name FROM {self.inventory_system.fields_table}")
            fields = [row[0] for row in self.inventory_system.cursor.fetchall()]

            # Display the list of fields
            tk.Label(popup, text="Existing Fields:").pack(pady=10)
            fields_label = tk.Label(popup, text="\n".join(fields), justify=tk.LEFT)
            fields_label.pack(pady=5)

            # Name of field to be removed
            tk.Label(popup, text="Field Name:").pack(pady=10)
            field_name_entry = tk.Entry(popup)
            field_name_entry.pack()

            def submit():
                field_name = field_name_entry.get()
                if field_name not in fields:
                    messagebox.showerror("Error", "Field name does not exist.")
                    return
                self.inventory_system.remove_to_fields_table(field_name)
                popup.destroy()

            # Button for executing the field removal
            submit_button = tk.Button(popup, text="Remove Field", command=submit, bg="#af4c4c", fg="white")
            submit_button.pack(pady=10)
            
         # Options Menu buttons (Add and Remove Field)
        add_field_button = tk.Button(window, text="Add Field", command=add_field_popup)
        add_field_button.pack(pady=10)

        remove_field_button = tk.Button(window, text="Remove Field", command=remove_field_popup)
        remove_field_button.pack(pady=10)       
        
        
        
    #   MENU
    #       - Display Inventory (see all products in database table)
    #       - Add/Remove Product
    #       - Options (add or remove field)
    #       - Clear Database (for testing)
    #       - Exit (quit the program)
    def display_menu(self):
        root = tk.Tk()
        root.title(self.inventory_system.name)
        root.geometry("700x700")
        root.configure(bg="#f0f0f0")  # Set background color
        
        # Create title frame
        title_frame = Frame(root, bg="#3498db", pady=15)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text=self.inventory_system.name, 
                            font=("Consolas", 16, "bold"), bg="#3498db", fg="white")
        title_label.pack()
        
        # Create main content frame
        content_frame = Frame(root, bg="#f0f0f0", pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons with better styling
        button_style = {"font": ("Consolas", 11),
                    "bg": "#2980b9",
                    "fg": "white",
                    "width": 20,
                    "height": 2,
                    "borderwidth": 0,
                    "cursor": "hand2"}
        
        tk.Button(content_frame, text="Display Inventory", command=self.inventory_system.display_inventory, 
                **button_style).pack(pady=10)
        
        tk.Button(content_frame, text="Add Product", command=self.inventory_system.add_item,
                **button_style).pack(pady=10)
        
        tk.Button(content_frame, text="Remove Product", command=self.inventory_system.remove_item,
                **button_style).pack(pady=10)
        
        tk.Button(content_frame, text="Options", command=self.inventory_system.display_options,
                bg="gray", fg="white", font=("Consolas", 11),
                width=20, height=2, borderwidth=0).pack(pady=20)
        
        tk.Button(content_frame, text="Clear Database", command=self.inventory_system.clear_database,
                bg="black", fg="white", font=("Consolas", 11),
                width=20, height=2, borderwidth=0).pack(pady=20)
        
        tk.Button(content_frame, text="Exit", command=root.quit,
                bg="#e74c3c", fg="white", font=("Consolas", 11),
                width=20, height=2, borderwidth=0).pack(pady=20)
        
        # Add status bar
        status_bar = tk.Label(root, text="Inventory Online", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        root.mainloop()
