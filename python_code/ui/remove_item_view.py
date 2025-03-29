import customtkinter as ctk
from tkinter import messagebox
import re

class RemoveItemView:
    def __init__(self, parent, inventory_system, patterns):
        self.window = ctk.CTkToplevel(parent)
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
        header = ctk.CTkFrame(self.window, fg_color=colors['warning'], corner_radius=0)
        header.pack(fill=ctk.X)
        
        ctk.CTkLabel(header, 
               text="Remove Product", 
               font=("Segoe UI", 14, "bold"),
               text_color="white").pack(padx=20, pady=15)
        
        # Main container
        main_container = ctk.CTkFrame(self.window, fg_color=colors['bg'], corner_radius=0)
        main_container.pack(fill=ctk.BOTH, expand=True, padx=40, pady=30)
        
        # ID field
        id_frame = ctk.CTkFrame(main_container, fg_color=colors['bg'])
        id_frame.pack(fill=ctk.X, pady=15)
        
        ctk.CTkLabel(id_frame, 
               text="Item ID", 
               font=("Segoe UI", 11, "bold"),
               text_color=colors['text']).pack(anchor="w")
        
        self.id_entry = ctk.CTkEntry(id_frame, 
                              font=("Segoe UI", 11),
                              width=400)
        self.id_entry.pack(fill=ctk.X, pady=5)
        
        ctk.CTkLabel(id_frame, 
               text="Enter the ID of the item you want to remove", 
               font=("Segoe UI", 9),
               text_color="#666666").pack(anchor="w")
        
        # Count field
        count_frame = ctk.CTkFrame(main_container, fg_color=colors['bg'])
        count_frame.pack(fill=ctk.X, pady=15)
        
        ctk.CTkLabel(count_frame, 
               text="Quantity", 
               font=("Segoe UI", 11, "bold"),
               text_color=colors['text']).pack(anchor="w")
        
        self.count_entry = ctk.CTkEntry(count_frame, 
                                 font=("Segoe UI", 11),
                                 width=400)
        self.count_entry.pack(fill=ctk.X, pady=5)
        
        ctk.CTkLabel(count_frame, 
               text="Enter the number of items to remove", 
               font=("Segoe UI", 9),
               text_color="#666666").pack(anchor="w")
        
        # Warning message
        warning_frame = ctk.CTkFrame(main_container, fg_color=colors['bg'])
        warning_frame.pack(fill=ctk.X, pady=15)
        
        ctk.CTkLabel(warning_frame, 
               text="Warning: This action cannot be undone.", 
               font=("Segoe UI", 10, "italic"),
               text_color=colors['warning']).pack(anchor="w")
        
        # Buttons container
        button_frame = ctk.CTkFrame(self.window, fg_color=colors['light_bg'], corner_radius=0)
        button_frame.pack(fill=ctk.X, side=ctk.BOTTOM, pady=15)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(button_frame, 
                             text="Cancel", 
                             command=self.window.destroy,
                             font=("Segoe UI", 10),
                             fg_color="white",
                             text_color=colors['text'])
        cancel_btn.pack(side=ctk.LEFT, padx=20)
        
        # Remove button
        remove_btn = ctk.CTkButton(button_frame, 
                             text="Remove Item", 
                             command=self.remove_item,
                             font=("Segoe UI", 10, "bold"),
                             fg_color=colors['danger'],
                             text_color="white")
        remove_btn.pack(side=ctk.RIGHT, padx=20)
        
        # Footer with watermark
        ctk.CTkLabel(button_frame, 
               text="Made by CodeByte",
               font=("Segoe UI", 8, "italic"),
               text_color="#a0a0a0").pack(side=ctk.BOTTOM, pady=(15, 0))
        
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