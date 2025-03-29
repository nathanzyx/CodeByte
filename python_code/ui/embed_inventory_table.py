import customtkinter as ctk
from tkinter import ttk

#
# Embed Inventory Table Class is initialized with a function that returns a dataframe
# This class embeds a table in a UI window
#
class EmbedInventoryTable:
    def __init__(self, parent, function):
        self.parent = parent
        self.df = function()
        # Dataframe columns and rows
        self.columns = self.df.columns.tolist()
        self.rows = self.df.values.tolist()
        
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
        header_frame = ctk.CTkFrame(self.parent, fg_color="#363062", corner_radius=0)
        header_frame.pack(fill=ctk.X, padx=20, pady=15)
                
        # Main container for the table
        container = ctk.CTkFrame(self.parent, fg_color="white", corner_radius=0)
        container.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
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
        y_scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=self.tree.yview)
        x_scrollbar = ctk.CTkScrollbar(container, orientation="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=y_scrollbar.set, xscroll=x_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        self.tree.pack(expand=True, fill="both")
        
        footer = ctk.CTkFrame(self.parent, fg_color="#f0f2f5", corner_radius=0)
        footer.pack(fill=ctk.X, side=ctk.BOTTOM, padx=10, pady=5)
        
        watermark = ctk.CTkLabel(footer, 
                                 text="Made by CodeByte",
                                 font=("Segoe UI", 8, "italic"),
                                 text_color="#a0a0a0")
        watermark.pack(side=ctk.RIGHT)
        
    def update_table(self, new_df):
        self.df = new_df
        self.columns = self.df.columns.tolist()
        self.rows = self.df.values.tolist()

        # Clear existing items from the table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add the new items from the search results
        for row in self.rows:
            self.tree.insert("", "end", values=row)

        # Reset the row colors
        for i, item in enumerate(self.tree.get_children()):
            self.tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow',))
