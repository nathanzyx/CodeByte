import customtkinter as ctk
from tkinter import messagebox
from ui.embed_inventory_table_edit import EmbedInventoryTableEdit

class SearchViewEdit:
    def __init__(self, parent, logic, inventory_system):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Manage Fields")
        self.window.geometry("1080x600")
        self.logic = logic
        self.inventory_system = inventory_system
        
        # search_results_table holds the Search Results table object from the EmbedInventoryTable class (initialized to None)
        self.search_results_table = None
        
        # This variable keeps all fields the user selects to search in
        self.selected_fields = []
        
        self.colors = {
            'primary': '#363062',
            'secondary': '#363062',
            'success': '#4F959D',
            'danger': '#f44336',
            'bg': '#ffffff',
            'text': '#2c3e50',
            'light_bg': '#f5f7fa',
            'untoggled': '#ffb0b0',
            'toggled': '#beffb0',
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self.window, fg_color=self.colors['secondary'], corner_radius=0)
        header.pack(fill=ctk.X)
        ctk.CTkLabel(header, 
            text="Search & Modify Database", 
            font=("Segoe UI", 14, "bold"),
            text_color="white").pack(padx=20, pady=15)
        
        # Main Container
        main_container = ctk.CTkFrame(self.window, fg_color=self.colors['bg'], corner_radius=0)
        main_container.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # SEARCH BAR
        search_frame = ctk.CTkFrame(main_container, fg_color=self.colors['bg'], corner_radius=0)
        search_frame.pack(fill=ctk.X, pady=(0, 15))
        search_frame.grid_columnconfigure(0, weight=1)
        self.search_entry = ctk.CTkEntry(search_frame, font=("Segoe UI", 12), width=400, justify="center")
        self.search_entry.grid(row=0, column=0, padx=10)
        self.search_entry.bind("<KeyRelease>", 
        lambda event: self.on_search(self.search_entry.get()))
        
        # FIELDS BAR
        fields_frame = ctk.CTkFrame(main_container, fg_color=self.colors['bg'], corner_radius=0)
        fields_frame.pack(fill=ctk.X, pady=(0, 15))
        
        # SELECT ALL
        self.selected_fields = set()
        self.field_buttons = {}  # Dictionary to store buttons for toggling state
        
        # Button to select all fields
        select_all_btn = ctk.CTkButton(fields_frame, text="Select All",
            command=self.toggle_select_all, font=("Segoe UI", 10), fg_color=self.colors['success'], text_color="white")
        select_all_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Get existing fields
        fields = self.logic.get_existing_fields()
        
        # Columns for field selections (Formatting), Starts at row 1 since row 0 is for the select all button
        columns_per_row = 5
        start_row = 1

        for idx, field in enumerate(fields):
            btn = ctk.CTkButton(fields_frame, text=field,
                        command=lambda f=field: self.toggle_field(f),
                        fg_color=self.colors['toggled'], font=("Segoe UI", 10), text_color=self.colors['text'])
            row = start_row + idx // columns_per_row
            col = idx % columns_per_row
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            self.field_buttons[field] = btn
            self.selected_fields.add(field)
        
        # CENTERING COLUMNS
        total_columns = columns_per_row
        for col in range(total_columns):
            fields_frame.grid_columnconfigure(col, weight=1)

        # Results Frame (For Table of search results)
        self.results_frame = ctk.CTkFrame(main_container, fg_color="#ffffff", corner_radius=0)
        self.results_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # Make initial search to display all items
        self.on_search(self.search_entry.get())
        
    def toggle_field(self, field):
        if field in self.selected_fields:
            # DESELECT
            self.selected_fields.remove(field)
            self.field_buttons[field].configure(fg_color=self.colors['untoggled'], text_color="black")
        else:
            # SELECT
            self.selected_fields.add(field)
            self.field_buttons[field].configure(fg_color=self.colors['toggled'], text_color="black")

    def toggle_select_all(self):
        if len(self.selected_fields) == len(self.field_buttons):
            # DESELECT
            self.selected_fields.clear()
            for field, btn in self.field_buttons.items():
                btn.configure(fg_color=self.colors['untoggled'], text_color="black")
        else:
            # SELECT
            self.selected_fields = set(self.field_buttons.keys())
            for field, btn in self.field_buttons.items():
                btn.configure(fg_color=self.colors['toggled'], text_color="black")
    
    def modify_item(self, item_data):
        if not item_data:
            return

        mod_window = ctk.CTkToplevel(self.window)
        mod_window.title("Modify Product")
        mod_window.geometry("400x400")
        
        columns = self.search_results_table.columns
        entries = {}
        
        for idx, col in enumerate(columns):
            ctk.CTkLabel(mod_window, text=col.capitalize(), font=("Segoe UI", 10, "bold")
                    ).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(mod_window, font=("Segoe UI", 10))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[col] = entry
        
        for col, value in zip(columns, item_data):
            entries[col].insert(0, str(value))
        
        def save_changes():
            new_data = {col: entries[col].get() for col in columns}
            product_id = item_data[0]
            
            success = self.inventory_system.update_item(product_id, new_data)
            if success:
                mod_window.destroy()
                self.on_search(self.search_entry.get())
            else:
                messagebox.showerror("Error", "Failed to update the product.")

        save_btn = ctk.CTkButton(mod_window, text="Save Changes", font=("Segoe UI", 10, "bold"),
                        command=save_changes, fg_color=self.colors['primary'], text_color="white")
        save_btn.grid(row=len(columns), column=1, pady=20)
    
    def on_search(self, query):
        if self.search_results_table:
            self.search_results_table.update_table(
                self.inventory_system.search_items(self.selected_fields, query))
        else:
            self.search_results_table = EmbedInventoryTableEdit(
                self.results_frame, 
                lambda: self.inventory_system.search_items(self.selected_fields, query),
                modify_callback=self.modify_item
            )