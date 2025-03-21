import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Frame
from datetime import datetime
import re
from ui.ui_logic import UILogic
from ui.embed_inventory_table import EmbedInventoryTable
from ui.search_view import SearchView
from ui.login_view import LoginView
from ui.display_default import DisplayDefault
from ui.add_item_view import AddItemView
from ui.remove_item_view import RemoveItemView
from ui.manage_fields_view import ManageFieldsView

#   UI Class
#
#   This class is for the UI of a database instance
#

class UI:
    def __init__(self, inventory_system):
        self.inventory_system = inventory_system
        self.logic = UILogic(inventory_system)
        self.patterns = self.logic.patterns
    
    #
    #   This function returns the users login status along with a message if not logged in
    #
    def is_logged_in(self):
        if not self.inventory_system.logged_in:
            messagebox.showerror("Login Required", "You must be logged in to perform this action.")
            return False
        return True
        
    #
    #   This function takes all column names from the 'product' table and displays the data
    #
    def display_inventory(self):
        # Always allow viewing inventory (no login required)
        DisplayDefault(tk._default_root, self.inventory_system.get_all_items)
        
    def display_search(self):
        if not self.is_logged_in():
            return
        SearchView(tk._default_root, self.logic, self.inventory_system)
    
    #
    #   This function:
    #           - takes field inputs from field table to prompt the user to input necessary information 
    #           - Upon submitting, calls function from DatabaseSystem class to add the item to the inventory
    #
    def display_add_item(self):
        if not self.is_logged_in():
            return
        AddItemView(tk._default_root, self.logic, self.inventory_system)
        # self.inventory_system.add_log_entry("Item added", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    #   REMOVE ITEM UI
    #       User Enters:
    #               - ID of Item to be Removed
    #               - Number of that Item to be Removed (int)
    def display_remove_item(self):
        if not self.is_logged_in():
            return
        RemoveItemView(tk._default_root, self.inventory_system, self.patterns)
        # self.inventory_system.add_log_entry("Item removed", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
    #   OPTIONS MENU    
    #       - Add Field (for adding product field)
    #       - Remove Field (for removing product field)
    #
    def display_options(self):
        if not self.is_logged_in():
            return
        ManageFieldsView(tk._default_root, self.logic, self.inventory_system)
        
    def display_login(self):
        if not self.inventory_system.logged_in():
            LoginView(tk._default_root, self.logic, self.inventory_system)
        
    #   MENU
    #       - Display Inventory (see all products in database table)
    #       - Add/Remove Product
    #       - Options (add or remove field)
    #       - Clear Database (for testing)
    #       - Exit (quit the program)
    def display_menu(self):
            
        root = tk.Tk()
        root.title(self.inventory_system.name)
        root.geometry("1200x800")
        root.configure(bg="#f0f2f5")

        # Define color scheme
        colors = {
            'bg': '#f0f2f5',
            'sidebar': '#ffffff',
            'primary': '#363062',
            'secondary': '#424242',
            'accent': '#2196f3',
            'danger': '#f44336',
            'text': '#2c3e50',
            'subtext': '#666666'
        }

        # Create main container with sidebar and content area
        main_container = Frame(root, bg=colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        sidebar = Frame(main_container, bg=colors['sidebar'], width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0)
        sidebar.pack_propagate(False)  # Maintain width

        # Logo and title area
        logo_frame = Frame(sidebar, bg=colors['primary'], height=130)
        logo_frame.pack(fill=tk.X)
        
        logo_label = tk.Label(logo_frame, text="💻", font=("Arial", 28), bg=colors['primary'], fg="white")
        logo_label.pack(pady=(20, 0))
        
        # App name - take first word from inventory system name
        app_name = tk.Label(logo_frame, text=self.inventory_system.name.split()[0], 
                          font=("Segoe UI", 16, "bold"), bg=colors['primary'], fg="white")
        app_name.pack(pady=(0, 5))
        
        # Tagline
        tagline = tk.Label(logo_frame, text="Inventory System", font=("Segoe UI", 10), 
                         bg=colors['primary'], fg="#e0e0e0")
        tagline.pack(pady=(0, 10))
        

        # Navigation menu
        nav_frame = Frame(sidebar, bg=colors['sidebar'])
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=16)

        # Button style
        nav_btn_style = {
            "font": ("Segoe UI", 11),
            "width": 28,
            "height": 2,
            "anchor": "w",
            "bd": 0,
            "cursor": "hand2",
            "fg": colors['text'],
            "bg": colors['sidebar']
        }

        def create_nav_button(text, icon, command):
            btn = tk.Button(nav_frame, text=f" {icon}  {text}", command=command, **nav_btn_style)
            btn.pack(pady=4)
            
            def on_hover(e):
                e.widget['bg'] = colors['bg']
            def on_leave(e):
                e.widget['bg'] = colors['sidebar']
                
            btn.bind("<Enter>", on_hover)
            btn.bind("<Leave>", on_leave)
            return btn

        # Navigation buttons
        create_nav_button("View Inventory", "📊", self.display_inventory)
        create_nav_button("Search Inventory", "🔎", self.display_search)
        create_nav_button("Add Product", "➕", self.display_add_item)
        create_nav_button("Remove Product", "➖", self.display_remove_item)
        
        # Separator
        tk.Frame(nav_frame, height=2, bg=colors['bg']).pack(fill=tk.X, pady=20)
        
        create_nav_button("Manage Fields", "⚙️", self.display_options)
        create_nav_button("Clear Database", "🗑️", self.inventory_system.clear_database)
        
        # Exit button at bottom of sidebar
        exit_btn = tk.Button(sidebar, text=" 🚪  Exit Application",
                            command=root.quit,
                            font=("Segoe UI", 11),
                            fg="white",
                            bg=colors['danger'],
                            bd=0,
                            cursor="hand2",
                            width=28,
                            height=2)
        exit_btn.pack(side=tk.BOTTOM, pady=20)
        exit_btn = tk.Button(sidebar, text=" ✅  Login",
                            command=self.display_login,
                            font=("Segoe UI", 11),
                            fg="white",
                            bg="#969696",
                            bd=0,
                            cursor="hand2",
                            width=28,
                            height=2)
        exit_btn.pack(side=tk.BOTTOM, pady=20)

        # Add watermark below the exit button
        watermark = tk.Label(sidebar, 
                           text="Made by CodeByte",
                           font=("Segoe UI", 8, "italic"),
                           fg="#a0a0a0",
                           bg=colors['sidebar'])
        watermark.pack(side=tk.BOTTOM, pady=(0, 5))

        # Main content area
        content = Frame(main_container, bg=colors['bg'])
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Welcome card
        welcome_card = Frame(content, bg="white", padx=30, pady=30)
        welcome_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(welcome_card,
                text="Welcome to Your Inventory Dashboard",
                font=("Segoe UI", 20, "bold"),
                bg="white",
                fg=colors['text']).pack(anchor="w")
                
        tk.Label(welcome_card,
                text="Manage your inventory efficiently with our modern interface",
                font=("Segoe UI", 12),
                bg="white",
                fg=colors['subtext']).pack(anchor="w", pady=(10, 0))

        # Stats cards container
        stats_container = Frame(content, bg=colors['bg'])
        stats_container.pack(fill=tk.X, pady=20)
        
        # Create three stat cards
        def create_stat_card(title, value, icon):
            card = Frame(stats_container, bg="white", padx=20, pady=15)
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            tk.Label(card, text=icon, font=("Segoe UI", 24),
                    bg="white").pack(anchor="w")
            tk.Label(card, text=title, font=("Segoe UI", 11),
                    bg="white", fg=colors['subtext']).pack(anchor="w")
            tk.Label(card, text=value, font=("Segoe UI", 20, "bold"),
                    bg="white", fg=colors['text']).pack(anchor="w")

        # Add sample stats (you can replace these with real data)
        create_stat_card("Total Products", "--", "📦")
        create_stat_card("Low Stock Items", "--", "⚠️")
        create_stat_card("Total Value", "$--", "💰")

        # Footer
        footer = Frame(content, bg=colors['bg'])
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        
        current_time = datetime.now().strftime("%d %b %Y")
        version_label = tk.Label(footer,
                            text=f"v1.0 • {current_time}",
                            font=("Segoe UI", 9),
                            bg=colors['bg'],
                            fg=colors['subtext'])
        version_label.pack(side=tk.RIGHT)

        root.mainloop()

    def validate_input(self, value, validation_type, is_required, label, message_labels):
        if is_required and not value.strip():
            message_labels[label].config(text=f"{label} is required.")
            return False
        if not is_required and not value.strip():
            return True
        if validation_type == 'string' and not re.match(self.patterns['string'], value):
            message_labels[label].config(text=f"{label} contains invalid characters.")
            return False
        if validation_type == 'int' and not re.match(self.patterns['int'], value):
            message_labels[label].config(text=f"{label} must be an integer.")
            return False
        if validation_type == 'float' and not re.match(self.patterns['float'], value):
            message_labels[label].config(text=f"{label} must be a float (contain decimal point).")
            return False
        return True

