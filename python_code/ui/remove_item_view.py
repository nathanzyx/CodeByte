import tkinter as tk
from tkinter import messagebox, Frame
import re

class RemoveItemView:
    def __init__(self, parent, inventory_system, patterns):
        self.window = tk.Toplevel(parent)
        self.window.title("Remove Item")
        self.window.geometry("500x700")
        self.inventory_system = inventory_system
        self.patterns = patterns
        self.setup_ui()
        
    def setup_ui(self):
        # Colors
        colors = {
            'primary': '#363062',
            'danger': '#f44336',
            'warning': '#ff9800',
            'bg': '#ffffff',
            'text': '#2c3e50',
            'light_bg': '#f5f7fa'
        }
        
        # Header
        header = Frame(self.window, bg=colors['warning'], pady=15)
        header.pack(fill=tk.X)
        
        tk.Label(header, 
               text="Remove Product", 
               font=("Segoe UI", 14, "bold"),
               bg=colors['warning'],
               fg="white").pack(padx=20)
        
        # Main container
        main_container = Frame(self.window, bg=colors['bg'], padx=40, pady=30)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Form fields with improved layout
        
        # ID field
        id_frame = Frame(main_container, bg=colors['bg'], pady=15)
        id_frame.pack(fill=tk.X)
        
        tk.Label(id_frame, 
               text="Item ID", 
               font=("Segoe UI", 11, "bold"),
               bg=colors['bg'],
               fg=colors['text']).pack(anchor="w")
        
        self.id_entry = tk.Entry(id_frame, 
                              font=("Segoe UI", 11),
                              width=40,
                              relief=tk.SOLID,
                              bd=1)
        self.id_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(id_frame, 
               text="Enter the ID of the item you want to remove", 
               font=("Segoe UI", 9),
               bg=colors['bg'],
               fg="#666666").pack(anchor="w")
        
        # Count field
        count_frame = Frame(main_container, bg=colors['bg'], pady=15)
        count_frame.pack(fill=tk.X)
        
        tk.Label(count_frame, 
               text="Quantity", 
               font=("Segoe UI", 11, "bold"),
               bg=colors['bg'],
               fg=colors['text']).pack(anchor="w")
        
        self.count_entry = tk.Entry(count_frame, 
                                 font=("Segoe UI", 11),
                                 width=40,
                                 relief=tk.SOLID,
                                 bd=1)
        self.count_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(count_frame, 
               text="Enter the number of items to remove", 
               font=("Segoe UI", 9),
               bg=colors['bg'],
               fg="#666666").pack(anchor="w")
        
        # Warning message
        warning_frame = Frame(main_container, bg=colors['bg'], pady=15)
        warning_frame.pack(fill=tk.X)
        
        warning_msg = tk.Label(warning_frame, 
                            text="Warning: This action cannot be undone.", 
                            font=("Segoe UI", 10, "italic"),
                            bg=colors['bg'],
                            fg=colors['warning'])
        warning_msg.pack(anchor="w")
        
        # Buttons container
        button_frame = Frame(self.window, bg=colors['light_bg'], pady=15)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, 
                             text="Cancel", 
                             command=self.window.destroy,
                             font=("Segoe UI", 10),
                             bg="white",
                             fg=colors['text'],
                             padx=15,
                             pady=5,
                             relief=tk.SOLID,
                             bd=1)
        cancel_btn.pack(side=tk.LEFT, padx=20)
        
        # Remove button
        remove_btn = tk.Button(button_frame, 
                             text="Remove Item", 
                             command=self.remove_item,
                             font=("Segoe UI", 10, "bold"),
                             bg=colors['danger'],
                             fg="white",
                             padx=15,
                             pady=5,
                             relief=tk.FLAT)
        remove_btn.pack(side=tk.RIGHT, padx=20)
        
        # Footer with watermark
        watermark = tk.Label(button_frame, 
                          text="Made by CodeByte",
                          font=("Segoe UI", 8, "italic"),
                          fg="#a0a0a0",
                          bg=colors['light_bg'])
        watermark.pack(side=tk.BOTTOM, pady=(15, 0))
        
    def remove_item(self):
        # Get values
        item_id = self.id_entry.get().strip()
        item_count = self.count_entry.get().strip()
        
        if not re.match(self.patterns['int'], item_count):
            messagebox.showerror("Error", "Invalid Count. Please enter a number.")
            return

        if not item_id:
            messagebox.showerror("Error", "Please enter a valid item ID.")
            return

        try:
            # Try to remove the item from the database
            self.inventory_system.remove_item_from_database(item_id, item_count)
            self.window.destroy()
            messagebox.showinfo("Success", f"Item with ID {item_id} removed successfully.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))