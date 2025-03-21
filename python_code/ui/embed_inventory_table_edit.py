import tkinter as tk
from tkinter import ttk, Frame

#
# Embed Inventory Table Class is initialized with a function that returns a dataframe
# This class is embeds a table in a UI window
#
class EmbedInventoryTableEdit:
    def __init__(self, parent, function, modify_callback = None):
        self.parent = parent
        self.df = function()
        # Dataframes columns and rows
        self.columns = self.df.columns.tolist()
        self.rows = self.df.values.tolist()
        self.modify_callback = modify_callback
        
        self.colors = {
            'primary': '#363062',
            'danger': '#f44336',
            'warning': '#ff9800',
            'bg': '#ffffff',
            'text': '#2c3e50',
            'light_bg': '#f5f7fa'
        }
        
        self.setup_ui()
        
        
    def setup_ui(self):
        # Set modern style for the treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview", 
                        background=self.colors['bg'],
                        foreground="#212529",
                        rowheight=25,
                        fieldbackground=self.colors['bg'])
        
        # Create header frame inside the parent
        header_frame = Frame(self.parent, bg="#363062", padx=20, pady=15)
        header_frame.pack(fill=tk.X)
                
        # Main container for the table
        container = Frame(self.parent, bg="white", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create the treeview widget with the appropriate columns
        self.tree = ttk.Treeview(container, columns=self.columns, show="headings")
        
        # Columns for table format
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize(), anchor='center')
            self.tree.column(col, anchor='center', width=100)
        # Rows for table format
        for row in self.rows:
            self.tree.insert("", "end", values=row)
            
        # Add Initial row colors
        self.tree.tag_configure('oddrow', background='#f8f9fa')
        self.tree.tag_configure('evenrow', background='#e9ecef')
        for i, item in enumerate(self.tree.get_children()):
            self.tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow',))
        
        # ENABLE SCROLLING
        y_scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=y_scrollbar.set, xscroll=x_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        self.tree.pack(expand=True, fill="both")
        
        footer = Frame(self.parent, bg="#f0f2f5", padx=10, pady=5)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        watermark = tk.Label(footer, 
                             text="Made by CodeByte",
                             font=("Segoe UI", 8, "italic"),
                             fg="#a0a0a0",
                             bg="#f0f2f5")
        watermark.pack(side=tk.RIGHT)
        
        if self.modify_callback is not None:
            self.tree.bind("<Double-1>", lambda event: self.modify_callback(self.get_selected_item()))
    
    def get_selected_item(self):
        selected_item = self.tree.focus()
        if selected_item:
            return self.tree.item(selected_item)['values']
        return None
    
    def update_table(self, new_df):
        self.df = new_df
        self.columns = self.df.columns.tolist()
        self.rows = self.df.values.tolist()

        # Clear existing items form the table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add the new items from the search results
        for row in self.rows:
            self.tree.insert("", "end", values=row)

        # Reset the row colors
        for i, item in enumerate(self.tree.get_children()):
            self.tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow',))
