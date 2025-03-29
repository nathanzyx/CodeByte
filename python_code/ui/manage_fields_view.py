import customtkinter as ctk
from tkinter import messagebox

class ManageFieldsView:
    def __init__(self, parent, logic, inventory_system):
        self.window = ctk.CTkToplevel(parent)
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
        header = ctk.CTkFrame(self.window, fg_color=colors['secondary'], corner_radius=0)
        header.pack(fill=ctk.X)
        
        ctk.CTkLabel(header, 
               text="Manage Database Fields", 
               font=("Segoe UI", 14, "bold"),
               text_color="white").pack(padx=20, pady=15)
        
        # Main container using tabs
        tab_control = ctk.CTkFrame(self.window, fg_color=colors['bg'], corner_radius=0)
        tab_control.pack(fill=ctk.BOTH, expand=True)
        
        # Tab buttons
        tab_frame = ctk.CTkFrame(tab_control, fg_color=colors['bg'], corner_radius=0)
        tab_frame.pack(fill=ctk.X)
        
        # Tab styling
        tab_style = {
            "font": ("Segoe UI", 10),
            "corner_radius": 0,
        }
        
        # Create references to tabs before using them in functions
        add_tab = ctk.CTkFrame(tab_control, fg_color=colors['bg'], corner_radius=0)
        remove_tab = ctk.CTkFrame(tab_control, fg_color=colors['bg'], corner_radius=0)
        
        def show_add_tab():
            add_tab.pack(fill=ctk.BOTH, expand=True, padx=40, pady=30)
            remove_tab.pack_forget()
            add_btn.configure(fg_color=colors['primary'], text_color="white")
            remove_btn.configure(fg_color="#e0e0e0", text_color=colors['text'])
            
        def show_remove_tab():
            remove_tab.pack(fill=ctk.BOTH, expand=True, padx=40, pady=30)
            add_tab.pack_forget()
            remove_btn.configure(fg_color=colors['primary'], text_color="white")
            add_btn.configure(fg_color="#e0e0e0", text_color=colors['text'])
        
        add_btn = ctk.CTkButton(tab_frame, text="Add Field", command=show_add_tab, 
                          **tab_style, fg_color=colors['primary'], text_color="white",
                          width=120, height=36)
        add_btn.pack(side=ctk.LEFT)
        
        remove_btn = ctk.CTkButton(tab_frame, text="Remove Field", command=show_remove_tab, 
                             **tab_style, fg_color="#e0e0e0", text_color=colors['text'],
                             width=120, height=36)
        remove_btn.pack(side=ctk.LEFT)
        
        # Add Field tab
        add_tab.pack(fill=ctk.BOTH, expand=True, padx=40, pady=30)
        
        # Field name
        ctk.CTkLabel(add_tab, 
               text="Field Name", 
               font=("Segoe UI", 11, "bold"),
               text_color=colors['text']).pack(anchor="w", pady=(0, 5))
        
        self.field_name_entry = ctk.CTkEntry(add_tab, 
                                      font=("Segoe UI", 10),
                                      width=400)
        self.field_name_entry.pack(fill=ctk.X, pady=(0, 15))
        
        # Entry type
        ctk.CTkLabel(add_tab, 
               text="Entry Type", 
               font=("Segoe UI", 11, "bold"),
               text_color=colors['text']).pack(anchor="w", pady=(10, 5))
        
        self.entry_type = ctk.StringVar()
        
        entry_frame = ctk.CTkFrame(add_tab, fg_color=colors['bg'], corner_radius=0)
        entry_frame.pack(fill=ctk.X, pady=(0, 15))
        
        small_box_btn = ctk.CTkButton(entry_frame, 
                                text="Small Box", 
                                command=lambda: self.entry_type.set("small_box"),
                                font=("Segoe UI", 10),
                                fg_color=colors['light_bg'],
                                text_color=colors['text'],
                                corner_radius=4,
                                height=32,
                                width=100)
        small_box_btn.pack(side=ctk.LEFT, padx=(0, 10))
        
        large_box_btn = ctk.CTkButton(entry_frame, 
                                text="Large Box", 
                                command=lambda: self.entry_type.set("large_box"),
                                font=("Segoe UI", 10),
                                fg_color=colors['light_bg'],
                                text_color=colors['text'],
                                corner_radius=4,
                                height=32,
                                width=100)
        large_box_btn.pack(side=ctk.LEFT)
        
        # Validation type
        ctk.CTkLabel(add_tab, 
               text="Validation Type", 
               font=("Segoe UI", 11, "bold"),
               text_color=colors['text']).pack(anchor="w", pady=(10, 5))
        
        self.validation_type = ctk.StringVar()
        
        validation_frame = ctk.CTkFrame(add_tab, fg_color=colors['bg'], corner_radius=0)
        validation_frame.pack(fill=ctk.X, pady=(0, 15))
        
        string_btn = ctk.CTkButton(validation_frame, 
                             text="String", 
                             command=lambda: self.validation_type.set("string"),
                             font=("Segoe UI", 10),
                             fg_color=colors['light_bg'],
                             text_color=colors['text'],
                             corner_radius=4,
                             height=32,
                             width=80)
        string_btn.pack(side=ctk.LEFT, padx=(0, 10))
        
        int_btn = ctk.CTkButton(validation_frame, 
                          text="Integer", 
                          command=lambda: self.validation_type.set("int"),
                          font=("Segoe UI", 10),
                          fg_color=colors['light_bg'],
                          text_color=colors['text'],
                          corner_radius=4,
                          height=32,
                          width=80)
        int_btn.pack(side=ctk.LEFT, padx=(0, 10))
        
        float_btn = ctk.CTkButton(validation_frame, 
                            text="Decimal", 
                            command=lambda: self.validation_type.set("float"),
                            font=("Segoe UI", 10),
                            fg_color=colors['light_bg'],
                            text_color=colors['text'],
                            corner_radius=4,
                            height=32,
                            width=80)
        float_btn.pack(side=ctk.LEFT)
        
        # Required
        ctk.CTkLabel(add_tab, 
               text="Is Required", 
               font=("Segoe UI", 11, "bold"),
               text_color=colors['text']).pack(anchor="w", pady=(10, 5))
        
        self.required = ctk.StringVar()
        
        required_frame = ctk.CTkFrame(add_tab, fg_color=colors['bg'], corner_radius=0)
        required_frame.pack(fill=ctk.X, pady=(0, 15))
        
        required_btn = ctk.CTkButton(required_frame, 
                              text="Required", 
                              command=lambda: self.required.set("1"),
                              font=("Segoe UI", 10),
                              fg_color=colors['light_bg'],
                              text_color=colors['text'],
                              corner_radius=4,
                              height=32,
                              width=100)
        required_btn.pack(side=ctk.LEFT, padx=(0, 10))
        
        not_required_btn = ctk.CTkButton(required_frame, 
                                  text="Not Required", 
                                  command=lambda: self.required.set("0"),
                                  font=("Segoe UI", 10),
                                  fg_color=colors['light_bg'],
                                  text_color=colors['text'],
                                  corner_radius=4,
                                  height=32,
                                  width=100)
        not_required_btn.pack(side=ctk.LEFT)
        
        # Add Field button
        add_field_btn = ctk.CTkButton(add_tab, 
                                text="Add Field", 
                                command=self.add_field,
                                font=("Segoe UI", 10, "bold"),
                                fg_color=colors['success'],
                                text_color="white",
                                height=36,
                                width=120,
                                corner_radius=4)
        add_field_btn.pack(pady=20)
        
        # Remove Field tab
        # Note: don't pack it here, it will be packed by the tab switch function
        
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
        ctk.CTkLabel(remove_tab, 
               text="Existing Fields", 
               font=("Segoe UI", 11, "bold"),
               text_color=colors['text']).pack(anchor="w", pady=(0, 10))
        
        # Create a container for the scrollable area
        fields_container = ctk.CTkFrame(remove_tab, fg_color=colors['bg'], corner_radius=0)
        fields_container.pack(fill=ctk.BOTH, expand=True, pady=(0, 20))
        
        # Use CTkScrollableFrame instead of canvas+scrollbar setup
        scrollable_frame = ctk.CTkScrollableFrame(fields_container, 
                                                 fg_color="#f0f2f5", 
                                                 corner_radius=4)
        scrollable_frame.pack(fill=ctk.BOTH, expand=True)
        
        if existing_fields:
            # First show built-in fields with descriptions
            system_label = ctk.CTkLabel(scrollable_frame, 
                   text="System Fields (Cannot be removed):", 
                   font=("Segoe UI", 10, "bold"),
                   text_color=colors['secondary'])
            system_label.pack(fill=ctk.X, padx=5, pady=3, anchor="w")
                   
            for field in existing_fields:
                if field in built_in_fields:
                    field_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f2f5", corner_radius=0)
                    field_frame.pack(fill=ctk.X, pady=2)
                    
                    ctk.CTkLabel(field_frame, 
                           text=f"• {field}", 
                           font=("Segoe UI", 10, "bold"),
                           text_color=colors['text'],
                           width=120).pack(side=ctk.LEFT, padx=5)
                           
                    ctk.CTkLabel(field_frame, 
                           text=f"{built_in_fields[field]}", 
                           font=("Segoe UI", 9),
                           text_color="#666").pack(side=ctk.LEFT, fill=ctk.X, padx=5)
            
            # Then show custom fields
            custom_fields = [field for field in existing_fields if field not in built_in_fields]
            
            if custom_fields:
                custom_label = ctk.CTkLabel(scrollable_frame, 
                       text="Custom Fields:", 
                       font=("Segoe UI", 10, "bold"),
                       text_color=colors['secondary'])
                custom_label.pack(fill=ctk.X, padx=5, pady=10, anchor="w")
                       
                for field in custom_fields:
                    ctk.CTkLabel(scrollable_frame, 
                           text=f"• {field}", 
                           font=("Segoe UI", 10),
                           text_color=colors['text']).pack(fill=ctk.X, padx=5, pady=3, anchor="w")
            else:
                ctk.CTkLabel(scrollable_frame, 
                       text="No custom fields found", 
                       font=("Segoe UI", 9, "italic"),
                       text_color="#666").pack(fill=ctk.X, padx=5, pady=3)
        else:
            ctk.CTkLabel(scrollable_frame, 
                   text="No fields found", 
                   font=("Segoe UI", 10, "italic"),
                   text_color="#666").pack(pady=10)
        
        # Field to remove
        ctk.CTkLabel(remove_tab, 
               text="Field Name to Remove", 
               font=("Segoe UI", 11, "bold"),
               text_color=colors['text']).pack(anchor="w", pady=(10, 5))
        
        self.remove_field_entry = ctk.CTkEntry(remove_tab, 
                                        font=("Segoe UI", 10),
                                        width=400)
        self.remove_field_entry.pack(fill=ctk.X, pady=(0, 5))
        
        # Warning
        ctk.CTkLabel(remove_tab, 
               text="Warning: Removing a field will delete all associated data", 
               font=("Segoe UI", 9, "italic"),
               text_color=colors['danger']).pack(anchor="w", pady=(5, 20))
        
        # Remove field button
        remove_field_btn = ctk.CTkButton(remove_tab, 
                                  text="Remove Field", 
                                  command=self.remove_field,
                                  font=("Segoe UI", 10, "bold"),
                                  fg_color=colors['danger'],
                                  text_color="white",
                                  width=120,
                                  height=36,
                                  corner_radius=4)
        remove_field_btn.pack()
        
        # Footer with watermark
        footer = ctk.CTkFrame(self.window, fg_color=colors['light_bg'], corner_radius=0)
        footer.pack(fill=ctk.X, side=ctk.BOTTOM)
        
        watermark = ctk.CTkLabel(footer, 
                          text="Made by CodeByte",
                          font=("Segoe UI", 8, "italic"),
                          text_color="#a0a0a0")
        watermark.pack(side=ctk.RIGHT, padx=20, pady=10)
        
        # Initialize with add tab shown
        show_add_tab()
        
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