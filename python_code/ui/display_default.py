import tkinter as tk
from tkinter import ttk, Frame


#
# Display Default Class is initialized with a function that must return a dataframe
# This class can be is used for displaying any data as long as the given function returns a dataframe
#
class DisplayDefault:
    def __init__(self, parent, function):
        self.window = tk.Toplevel(parent)
        self.window.title("Inventory")
        self.window.geometry("900x600")
        self.df = function()
        self.columns = self.df.columns.tolist()
        self.rows = self.df.values.tolist()
        self.setup_ui()
        
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview", 
                        background="#f8f9fa",
                        foreground="#212529",
                        rowheight=25,
                        fieldbackground="#f8f9fa")
        style.configure("Treeview.Heading", 
                        font=('Segoe UI', 10, 'bold'),
                        background="#e9ecef", 
                        foreground="#495057")
        
        # Header Frame
        header_frame = Frame(self.window, bg="#363062", padx=20, pady=15)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, 
                text="Inventory Items", 
                font=("Segoe UI", 16, "bold"),
                bg="#363062",
                fg="white").pack(anchor="w")
                
        # Main Container
        container = Frame(self.window, bg="white", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Treeview in container with columns from the given functions dataframe
        self.tree = ttk.Treeview(container, columns=self.columns, show="headings")
        
        # Make columns
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize(), anchor='center')
            self.tree.column(col, anchor='center', width=100)
        
        # Insert inventory data into each row
        for rows in self.rows:
            self.tree.insert("", "end", values=rows)
            
        # Create alternating row colors
        self.tree.tag_configure('oddrow', background='#f8f9fa')
        self.tree.tag_configure('evenrow', background='#e9ecef')
        for i, item in enumerate(self.tree.get_children()):
            self.tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow',))
        
        # SCROLLBAR
        y_scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=y_scrollbar.set, xscroll=x_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        self.tree.pack(expand=True, fill="both")
        
        # Footer with watermark
        footer = Frame(self.window, bg="#f0f2f5", padx=10, pady=5)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        watermark = tk.Label(footer, 
                           text="Made by CodeByte",
                           font=("Segoe UI", 8, "italic"),
                           fg="#a0a0a0",
                           bg="#f0f2f5")
        watermark.pack(side=tk.RIGHT)