import tkinter as tk
from tkinter import messagebox, Frame, Scrollbar, Checkbutton, Button
from ui.embed_inventory_table import EmbedInventoryTable

class SearchView:
    def __init__(self, parent, logic, inventory_system):
        self.window = tk.Toplevel(parent)
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
        header = Frame(self.window, bg=self.colors['secondary'], pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, 
            text="Search Database", 
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['secondary'],
            fg="white").pack(padx=20)
        
        # Main Container
        main_container = Frame(self.window, bg=self.colors['bg'], padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # SEARCH BAR
        search_frame = Frame(main_container, bg=self.colors['bg'])
        search_frame.pack(fill=tk.X, pady=(0, 15))
        search_frame.grid_columnconfigure(0, weight=1)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 12), width=40, justify="center")
        self.search_entry.grid(row=0, column=0, padx=10)
        self.search_entry.bind("<KeyRelease>", 
        lambda event: self.on_search(self.search_entry.get()))
        
        # FIELDS BAR
        fields_frame = Frame(main_container, bg=self.colors['bg'])
        fields_frame.pack(fill=tk.X, pady=(0, 15))
        
        # SELECT ALL
        self.selected_fields = set()
        self.field_buttons = {}  # Dictionary to store buttons for toggling state
        
        # Button to select all fields
        select_all_btn = Button(fields_frame, text="Select All",
            command=self.toggle_select_all, relief="flat", font=("Segoe UI", 10), bg=self.colors['success'], fg="white")
        select_all_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Get existing fields
        fields = self.logic.get_existing_fields()
        
        # Columns for field selections (Formatting), Starts at row 1 since row 0 is for the select all button
        columns_per_row = 5
        start_row = 1

        for idx, field in enumerate(fields):
            btn = Button(fields_frame, text=field,
                        command=lambda f=field: self.toggle_field(f),
                        relief="flat", bg=self.colors['untoggled'], font=("Segoe UI", 10), fg=self.colors['text'])
            row = start_row + idx // columns_per_row
            col = idx % columns_per_row
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            self.field_buttons[field] = btn
        
        # CENTERING COLUMNS
        total_columns = columns_per_row
        for col in range(total_columns):
            fields_frame.grid_columnconfigure(col, weight=1)

        # Results Frame (For Table of search results)
        self.results_frame = Frame(main_container, bg="#ffffff")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        

    #
    # This function toggles the state of a field button (selected or unselected)
    #
    def toggle_field(self, field):
        if field in self.selected_fields:
            # DESELECT
            self.selected_fields.remove(field)
            self.field_buttons[field].config(bg=self.colors['untoggled'], fg="black")
        else:
            # SELECT
            self.selected_fields.add(field)
            self.field_buttons[field].config(bg=self.colors['toggled'], fg="black")


    #
    # This function toggles the state of all field buttons (all selected or unselected)
    #
    def toggle_select_all(self):
        if len(self.selected_fields) == len(self.field_buttons):
            # DESELECT
            self.selected_fields.clear()
            for field, btn in self.field_buttons.items():
                btn.config(bg=self.colors['untoggled'], fg="black")
        else:
            # SELECT
            self.selected_fields = set(self.field_buttons.keys())
            for field, btn in self.field_buttons.items():
                btn.config(bg=self.colors['toggled'], fg="black")
    
    #
    # This function is called whenever the user types in the search bar:
    #   - Creates Search results object (table) if it doesnt exist
    #   - Updates the search results table with the new search results if it exists
    #
    def on_search(self, query):
        if self.search_results_table:
            # If the search table already exists, update it with the new search results
            self.search_results_table.update_table(self.inventory_system.search_items(self.selected_fields, query))
        else:
            # If the search table doesnt exists, we create a new instance of it for our window
            self.search_results_table = EmbedInventoryTable(self.results_frame, 
                                                     lambda: self.inventory_system.search_items(self.selected_fields, query))