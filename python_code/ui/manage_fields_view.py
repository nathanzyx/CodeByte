import tkinter as tk
from tkinter import messagebox, Frame, Scrollbar

class ManageFieldsView:
    def __init__(self, parent, logic, inventory_system):
        self.window = tk.Toplevel(parent)
        self.window.title("Manage Fields")
        self.window.geometry("500x700")
        self.logic = logic
        self.inventory_system = inventory_system
        self.setup_ui()
        
    def setup_ui(self):
        # Colors
        colors = {
            'primary': '#363062',
            'secondary': '#363062',
            'success': '#4F959D',
            'danger': '#f44336',
            'bg': '#ffffff',
            'text': '#2c3e50',
            'light_bg': '#f5f7fa'
        }
        
        # Header
        header = Frame(self.window, bg=colors['secondary'], pady=15)
        header.pack(fill=tk.X)
        
        tk.Label(header, 
               text="Manage Database Fields", 
               font=("Segoe UI", 14, "bold"),
               bg=colors['secondary'],
               fg="white").pack(padx=20)
        
        # Main container using tabs
        tab_control = tk.Frame(self.window, bg=colors['bg'])
        tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Tab buttons
        tab_frame = Frame(tab_control, bg=colors['bg'])
        tab_frame.pack(fill=tk.X)
        
        # Tab styling
        tab_style = {
            "font": ("Segoe UI", 10),
            "relief": tk.FLAT,
            "borderwidth": 0,
            "padx": 15,
            "pady": 10,
            "anchor": "center",
        }
        
        def show_add_tab():
            add_tab.pack(fill=tk.BOTH, expand=True)
            remove_tab.pack_forget()
            add_btn.config(bg=colors['primary'], fg="white")
            remove_btn.config(bg="#e0e0e0", fg=colors['text'])
            
        def show_remove_tab():
            remove_tab.pack(fill=tk.BOTH, expand=True)
            add_tab.pack_forget()
            remove_btn.config(bg=colors['primary'], fg="white")
            add_btn.config(bg="#e0e0e0", fg=colors['text'])
        
        add_btn = tk.Button(tab_frame, text="Add Field", command=show_add_tab, **tab_style, bg=colors['primary'], fg="white")
        add_btn.pack(side=tk.LEFT)
        
        remove_btn = tk.Button(tab_frame, text="Remove Field", command=show_remove_tab, **tab_style, bg="#e0e0e0", fg=colors['text'])
        remove_btn.pack(side=tk.LEFT)
        
        # Add Field tab
        add_tab = Frame(tab_control, bg=colors['bg'], padx=40, pady=30)
        add_tab.pack(fill=tk.BOTH, expand=True)
        
        # Field name
        tk.Label(add_tab, 
               text="Field Name", 
               font=("Segoe UI", 11, "bold"),
               bg=colors['bg'],
               fg=colors['text']).pack(anchor="w", pady=(0, 5))
        
        self.field_name_entry = tk.Entry(add_tab, 
                                      font=("Segoe UI", 10),
                                      width=40,
                                      relief=tk.SOLID,
                                      bd=1)
        self.field_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Entry type
        tk.Label(add_tab, 
               text="Entry Type", 
               font=("Segoe UI", 11, "bold"),
               bg=colors['bg'],
               fg=colors['text']).pack(anchor="w", pady=(10, 5))
        
        self.entry_type = tk.StringVar()
        
        entry_frame = Frame(add_tab, bg=colors['bg'])
        entry_frame.pack(fill=tk.X, pady=(0, 15))
        
        small_box_btn = tk.Button(entry_frame, 
                                text="Small Box", 
                                command=lambda: self.entry_type.set("small_box"),
                                font=("Segoe UI", 10),
                                bg=colors['light_bg'],
                                relief=tk.SOLID,
                                bd=1,
                                padx=10,
                                pady=5)
        small_box_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        large_box_btn = tk.Button(entry_frame, 
                                text="Large Box", 
                                command=lambda: self.entry_type.set("large_box"),
                                font=("Segoe UI", 10),
                                bg=colors['light_bg'],
                                relief=tk.SOLID,
                                bd=1,
                                padx=10,
                                pady=5)
        large_box_btn.pack(side=tk.LEFT)
        
        # Validation type
        tk.Label(add_tab, 
               text="Validation Type", 
               font=("Segoe UI", 11, "bold"),
               bg=colors['bg'],
               fg=colors['text']).pack(anchor="w", pady=(10, 5))
        
        self.validation_type = tk.StringVar()
        
        validation_frame = Frame(add_tab, bg=colors['bg'])
        validation_frame.pack(fill=tk.X, pady=(0, 15))
        
        string_btn = tk.Button(validation_frame, 
                             text="String", 
                             command=lambda: self.validation_type.set("string"),
                             font=("Segoe UI", 10),
                             bg=colors['light_bg'],
                             relief=tk.SOLID,
                             bd=1,
                             padx=10,
                             pady=5)
        string_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        int_btn = tk.Button(validation_frame, 
                          text="Integer", 
                          command=lambda: self.validation_type.set("int"),
                          font=("Segoe UI", 10),
                          bg=colors['light_bg'],
                          relief=tk.SOLID,
                          bd=1,
                          padx=10,
                          pady=5)
        int_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        float_btn = tk.Button(validation_frame, 
                            text="Decimal", 
                            command=lambda: self.validation_type.set("float"),
                            font=("Segoe UI", 10),
                            bg=colors['light_bg'],
                            relief=tk.SOLID,
                            bd=1,
                            padx=10,
                            pady=5)
        float_btn.pack(side=tk.LEFT)
        
        # Required
        tk.Label(add_tab, 
               text="Is Required", 
               font=("Segoe UI", 11, "bold"),
               bg=colors['bg'],
               fg=colors['text']).pack(anchor="w", pady=(10, 5))
        
        self.required = tk.StringVar()
        
        required_frame = Frame(add_tab, bg=colors['bg'])
        required_frame.pack(fill=tk.X, pady=(0, 15))
        
        required_btn = tk.Button(required_frame, 
                              text="Required", 
                              command=lambda: self.required.set("1"),
                              font=("Segoe UI", 10),
                              bg=colors['light_bg'],
                              relief=tk.SOLID,
                              bd=1,
                              padx=10,
                              pady=5)
        required_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        not_required_btn = tk.Button(required_frame, 
                                  text="Not Required", 
                                  command=lambda: self.required.set("0"),
                                  font=("Segoe UI", 10),
                                  bg=colors['light_bg'],
                                  relief=tk.SOLID,
                                  bd=1,
                                  padx=10,
                                  pady=5)
        not_required_btn.pack(side=tk.LEFT)
        
        # Add Field button
        add_field_btn = tk.Button(add_tab, 
                                text="Add Field", 
                                command=self.add_field,
                                font=("Segoe UI", 10, "bold"),
                                bg=colors['success'],
                                fg="white",
                                padx=15,
                                pady=8,
                                relief=tk.FLAT)
        add_field_btn.pack(pady=20)
        
        # Remove Field tab
        remove_tab = Frame(tab_control, bg=colors['bg'], padx=40, pady=30)
        
        # Get existing fields
        existing_fields = self.logic.get_existing_fields()
        
        # Define built-in fields that cannot be removed
        built_in_fields = {
            "brand": "Product manufacturer or brand name",
            "category": "Product category classification",
            "description": "Detailed product description",
            "id": "Unique product identifier",
            "name": "Product display name",
            "price": "Product retail price",
            "quantity": "Available inventory count"
        }
        
        # Display field list
        tk.Label(remove_tab, 
               text="Existing Fields", 
               font=("Segoe UI", 11, "bold"),
               bg=colors['bg'],
               fg=colors['text']).pack(anchor="w", pady=(0, 10))
        
        # Create a container for the scrollable area
        fields_container = Frame(remove_tab, bg=colors['bg'])
        fields_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Add a canvas for scrolling
        canvas = tk.Canvas(fields_container, bg="#f0f2f5", highlightthickness=0)
        scrollbar = Scrollbar(fields_container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#f0f2f5", padx=15, pady=15)
        
        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrolling components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        if existing_fields:
            # First show built-in fields with descriptions
            system_label = tk.Label(scrollable_frame, 
                   text="System Fields (Cannot be removed):", 
                   font=("Segoe UI", 10, "bold"),
                   bg="#f0f2f5",
                   fg=colors['secondary'],
                   anchor="w",
                   padx=5,
                   pady=3)
            system_label.pack(fill=tk.X)
                   
            for field in existing_fields:
                if field in built_in_fields:
                    field_frame = Frame(scrollable_frame, bg="#f0f2f5")
                    field_frame.pack(fill=tk.X, pady=2)
                    
                    tk.Label(field_frame, 
                           text=f"• {field}", 
                           font=("Segoe UI", 10, "bold"),
                           bg="#f0f2f5",
                           fg=colors['text'],
                           anchor="w",
                           width=15,
                           padx=5).pack(side=tk.LEFT)
                           
                    tk.Label(field_frame, 
                           text=f"{built_in_fields[field]}", 
                           font=("Segoe UI", 9),
                           bg="#f0f2f5",
                           fg="#666",
                           anchor="w",
                           padx=5).pack(side=tk.LEFT, fill=tk.X)
            
            # Then show custom fields
            custom_fields = [field for field in existing_fields if field not in built_in_fields]
            
            if custom_fields:
                # Fix the pady issue by using a single value
                custom_label = tk.Label(scrollable_frame, 
                       text="Custom Fields:", 
                       font=("Segoe UI", 10, "bold"),
                       bg="#f0f2f5",
                       fg=colors['secondary'],
                       anchor="w",
                       padx=5,
                       pady=10)  # Using a single value for pady
                custom_label.pack(fill=tk.X)
                       
                for field in custom_fields:
                    tk.Label(scrollable_frame, 
                           text=f"• {field}", 
                           font=("Segoe UI", 10),
                           bg="#f0f2f5",
                           fg=colors['text'],
                           anchor="w",
                           padx=5,
                           pady=3).pack(fill=tk.X)
            else:
                tk.Label(scrollable_frame, 
                       text="No custom fields found", 
                       font=("Segoe UI", 9, "italic"),
                       bg="#f0f2f5",
                       fg="#666",
                       padx=5,
                       pady=3).pack(fill=tk.X)
        else:
            tk.Label(scrollable_frame, 
                   text="No fields found", 
                   font=("Segoe UI", 10, "italic"),
                   bg="#f0f2f5",
                   fg="#666").pack(pady=10)
        
        # Field to remove
        tk.Label(remove_tab, 
               text="Field Name to Remove", 
               font=("Segoe UI", 11, "bold"),
               bg=colors['bg'],
               fg=colors['text']).pack(anchor="w", pady=(10, 5))
        
        self.remove_field_entry = tk.Entry(remove_tab, 
                                        font=("Segoe UI", 10),
                                        width=40,
                                        relief=tk.SOLID,
                                        bd=1)
        self.remove_field_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Warning
        tk.Label(remove_tab, 
               text="Warning: Removing a field will delete all associated data", 
               font=("Segoe UI", 9, "italic"),
               bg=colors['bg'],
               fg=colors['danger']).pack(anchor="w", pady=(5, 20))
        
        # Remove field button
        remove_field_btn = tk.Button(remove_tab, 
                                  text="Remove Field", 
                                  command=self.remove_field,
                                  font=("Segoe UI", 10, "bold"),
                                  bg=colors['danger'],
                                  fg="white",
                                  padx=15,
                                  pady=8,
                                  relief=tk.FLAT)
        remove_field_btn.pack()
        
        # Footer with watermark
        footer = Frame(self.window, bg=colors['light_bg'], pady=10)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        watermark = tk.Label(footer, 
                          text="Made by CodeByte",
                          font=("Segoe UI", 8, "italic"),
                          fg="#a0a0a0",
                          bg=colors['light_bg'])
        watermark.pack(side=tk.RIGHT, padx=20)
        
    def add_field(self):
        field_name = self.field_name_entry.get()
        entry_type_value = self.entry_type.get().strip()
        validation_type_value = self.validation_type.get().strip()
        required_value = self.required.get().strip()

        if self.logic.validate_field_specs(field_name, entry_type_value, validation_type_value, required_value):
            self.inventory_system.add_to_fields_table(field_name, entry_type_value, validation_type_value, int(required_value))
            messagebox.showinfo("Success", f"Field '{field_name}' added successfully.")
            self.window.destroy()
            
    def remove_field(self):
        field_name = self.remove_field_entry.get()
        fields = self.logic.get_existing_fields()
        
        # Define built-in fields that cannot be removed
        built_in_fields = ["brand", "category", "description", "id", "name", "price", "quantity"]
        
        if field_name not in fields:
            messagebox.showerror("Error", "Field name does not exist.")
            return
            
        if field_name in built_in_fields:
            messagebox.showerror("Error", f"'{field_name}' is a system field and cannot be removed.")
            return
            
        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Deletion", 
                                      f"Are you sure you want to remove the field '{field_name}'?\n\nThis will delete all associated data and cannot be undone.")
        
        if confirm:
            self.inventory_system.remove_to_fields_table(field_name)
            messagebox.showinfo("Success", f"Field '{field_name}' removed successfully.")
            self.window.destroy()