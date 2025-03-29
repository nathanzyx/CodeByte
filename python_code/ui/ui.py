import pandas as pd
import sys
import os
import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import re
from ui.ui_logic import UILogic
from ui.search_view_edit import SearchViewEdit
from ui.login_view import LoginView
from ui.display_default import DisplayDefault
from ui.add_item_view import AddItemView
from ui.remove_item_view import RemoveItemView
from ui.manage_fields_view import ManageFieldsView

from ui.embed_ai import EmbedAI
from ai.AI import AI 

#   UI Class
#    -  This class is for the UI of a database instance
#
class UI:
    def __init__(self, inventory_system):
        self.inventory_system = inventory_system
        self.ai = AI(inventory_system)
            
        self.logic = UILogic(inventory_system)
        self.patterns = self.logic.patterns
        self.crnt_user = "N/A"
        self.root = ctk.CTk()
        
        self.colors = {
            'bg': '#f0f2f5',
            'sidebar': '#ffffff',
            'primary': '#363062',
            'secondary': '#424242',
            'accent': '#2196f3',
            'danger': '#f44336',
            'text': '#2c3e50',
            'subtext': '#666666'
        }
        self.container = None
        self.content = None
        self.ai_frame = None

    #
    #   This function returns the users login status along with a message if not logged in
    #
    def is_logged_in(self):
        if not self.inventory_system.logged_in:
            messagebox.showerror("Login Required", "You must be logged in to perform this action.")
            return False
        return True
        
    def display_inventory(self):
        if not self.is_logged_in():
            return
        SearchViewEdit(self.root, self.logic, self.inventory_system)
    
    def display_add_item(self):
        if not self.is_logged_in():
            return
        AddItemView(self.root, self.logic, self.inventory_system)
        # self.inventory_system.add_log_entry("Item added", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    #   REMOVE ITEM UI
    #       User Enters:
    #               - ID of Item to be Removed
    #               - Number of that Item to be Removed (int)
    def display_remove_item(self):
        if not self.is_logged_in():
            return
        RemoveItemView(self.root, self.inventory_system, self.patterns)
        # self.inventory_system.add_log_entry("Item removed", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
    #   OPTIONS MENU    
    #       - Add Field (for adding product field)
    #       - Remove Field (for removing product field)
    #
    def display_options(self):
        if not self.is_logged_in():
            return
        ManageFieldsView(self.root, self.logic, self.inventory_system)
        
    def display_login(self):
        if not self.inventory_system.logged_in:
            LoginView(self.root, self.logic, self.inventory_system)
            
    def display_ai_assistant(self):
        EmbedAI(self.ai, self.ai_frame)
        
    def exit_application(self):
        # Perform any actions you want before exiting
        print("Closing App...")
        self.inventory_system.log_message(f" -- LOGOUT: user:{str(self.crnt_user)}")

        # Exit application
        self.root.quit()
    
    #   MENU
    #       - Display Inventory (see all products in database table)
    #       - Add/Remove Product
    #       - Options (add or remove field)
    #       - Clear Database (for testing)
    #       - Exit (quit the program)
    def display_menu(self):
        # Configure the main window
        self.root.title(self.inventory_system.name)
        self.root.geometry("1200x800")
        ctk.set_appearance_mode("light")  # Use light mode to match original style

        # Create main container with sidebar and content area
        self.container = ctk.CTkFrame(self.root, fg_color=self.colors['bg'], corner_radius=0)
        self.container.pack(fill=ctk.BOTH, expand=True)
        main_container = self.container

        # Sidebar
        sidebar = ctk.CTkFrame(main_container, fg_color=self.colors['sidebar'], width=280, corner_radius=0)
        sidebar.pack(side=ctk.LEFT, fill=ctk.Y, padx=0)
        sidebar.pack_propagate(False)  # Maintain width

        # Logo and title area
        logo_frame = ctk.CTkFrame(sidebar, fg_color=self.colors['primary'], height=130, corner_radius=0)
        logo_frame.pack(fill=ctk.X)
        
        logo_label = ctk.CTkLabel(logo_frame, text="💻", font=("Arial", 28), text_color="white")
        logo_label.pack(pady=(20, 0))
        
        # App name - take first word from inventory system name
        app_name = ctk.CTkLabel(logo_frame, text=self.inventory_system.name.split()[0], 
                          font=("Segoe UI", 16, "bold"), text_color="white")
        app_name.pack(pady=(0, 5))
        
        # Tagline
        tagline = ctk.CTkLabel(logo_frame, text="Inventory System", font=("Segoe UI", 10), 
                         text_color="#e0e0e0")
        tagline.pack(pady=(0, 10))
        
        # Navigation menu
        nav_frame = ctk.CTkFrame(sidebar, fg_color=self.colors['sidebar'], corner_radius=0)
        nav_frame.pack(fill=ctk.BOTH, expand=True, padx=16)

        # Button style
        nav_btn_style = {
            "font": ("Segoe UI", 11),
            "width": 250,
            "height": 40,
            "anchor": "w",
            "fg_color": self.colors['sidebar'],
            "text_color": self.colors['text'],
            "hover_color": self.colors['bg'],
            "corner_radius": 4
        }

        def create_nav_button(text, icon, command):
            btn = ctk.CTkButton(nav_frame, text=f" {icon}  {text}", command=command, **nav_btn_style)
            btn.pack(pady=4)
            return btn

        # Navigation buttons
        create_nav_button("Inventory", "📊", self.display_inventory)
        create_nav_button("Add Product", "➕", self.display_add_item)
        create_nav_button("Remove Product", "➖", self.display_remove_item)
        
        # Separator
        separator = ctk.CTkFrame(nav_frame, height=2, fg_color=self.colors['bg'], corner_radius=0)
        separator.pack(fill=ctk.X, pady=20)
        
        create_nav_button("Manage Fields", "⚙️", self.display_options)
        create_nav_button("Clear Database", "🗑️", self.inventory_system.clear_database)
        
        # Exit button at bottom of sidebar
        exit_btn = ctk.CTkButton(sidebar, text=" 🚪  Exit Application",
                            command=self.exit_application,
                            font=("Segoe UI", 11),
                            text_color="white",
                            fg_color=self.colors['danger'],
                            hover_color="#d32f2f",
                            corner_radius=4,
                            width=250,
                            height=40)
        exit_btn.pack(side=ctk.BOTTOM, pady=20)
        
        login_btn = ctk.CTkButton(sidebar, text=" ✅  Login",
                            command=self.display_login,
                            font=("Segoe UI", 11),
                            text_color="white",
                            fg_color="#969696",
                            hover_color="#7a7a7a",
                            corner_radius=4,
                            width=250,
                            height=40)
        login_btn.pack(side=ctk.BOTTOM, pady=20)

        # Add watermark below the exit button
        watermark = ctk.CTkLabel(sidebar, 
                           text="Made by CodeByte",
                           font=("Segoe UI", 8, "italic"),
                           text_color="#a0a0a0",
                           fg_color=self.colors['sidebar'])
        watermark.pack(side=ctk.BOTTOM, pady=(0, 5))

        # Main content area
        self.content = ctk.CTkFrame(self.container, fg_color=self.colors['bg'], corner_radius=0)
        self.content.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=30, pady=30)
        content = self.content

        # Welcome card
        welcome_card = ctk.CTkFrame(content, fg_color="white", corner_radius=6)
        welcome_card.pack(fill=ctk.X, pady=(0, 20), padx=5, ipady=20, ipadx=20)
        
        welcome_title = ctk.CTkLabel(welcome_card,
                text="Welcome to Your Inventory Dashboard",
                font=("Segoe UI", 20, "bold"),
                text_color=self.colors['text'])
        welcome_title.pack(anchor="w", padx=20, pady=(20, 0))
                
        welcome_subtitle = ctk.CTkLabel(welcome_card,
                text="Manage your inventory efficiently with our modern interface",
                font=("Segoe UI", 12),
                text_color=self.colors['subtext'])
        welcome_subtitle.pack(anchor="w", padx=20, pady=(10, 20))

        # Stats cards container
        stats_container = ctk.CTkFrame(content, fg_color=self.colors['bg'], corner_radius=0)
        stats_container.pack(fill=ctk.X, pady=20)
        
        # Create three stat cards
        def create_stat_card(title, value, icon):
            card = ctk.CTkFrame(stats_container, fg_color="white", corner_radius=6)
            card.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=5, ipady=10, ipadx=10)
            
            icon_label = ctk.CTkLabel(card, text=icon, font=("Segoe UI", 24),
                    fg_color="white", text_color=self.colors['text'])
            icon_label.pack(anchor="w", padx=20, pady=(15, 0))
            
            title_label = ctk.CTkLabel(card, text=title, font=("Segoe UI", 11),
                    fg_color="white", text_color=self.colors['subtext'])
            title_label.pack(anchor="w", padx=20)
            
            value_label = ctk.CTkLabel(card, text=value, font=("Segoe UI", 20, "bold"),
                    fg_color="white", text_color=self.colors['text'])
            value_label.pack(anchor="w", padx=20, pady=(0, 15))

        # Add sample stats (you can replace these with real data)
        create_stat_card("Total Products", "--", "📦")
        create_stat_card("Low Stock Items", "--", "⚠️")
        create_stat_card("Total Value", "$--", "💰")
        
        # AI Assistant section
        self.ai_frame = ctk.CTkFrame(self.content, fg_color="white", corner_radius=6)
        self.ai_frame.pack(fill=ctk.BOTH, expand=True, pady=(20, 0), padx=5)
        EmbedAI(self.ai, self.ai_frame)

        # Footer
        footer = ctk.CTkFrame(content, fg_color=self.colors['bg'], corner_radius=0)
        footer.pack(side=ctk.BOTTOM, fill=ctk.X)
        
        current_time = datetime.now().strftime("%d %b %Y")
        version_label = ctk.CTkLabel(footer,
                            text=f"v1.0 • {current_time}",
                            font=("Segoe UI", 9),
                            fg_color=self.colors['bg'],
                            text_color=self.colors['subtext'])
        version_label.pack(side=ctk.RIGHT)

        self.root.mainloop()

    def validate_input(self, value, validation_type, is_required, label, message_labels):
        if is_required and not value.strip():
            message_labels[label].configure(text=f"{label} is required.")
            return False
        if not is_required and not value.strip():
            return True
        if validation_type == 'string' and not re.match(self.patterns['string'], value):
            message_labels[label].configure(text=f"{label} contains invalid characters.")
            return False
        if validation_type == 'int' and not re.match(self.patterns['int'], value):
            message_labels[label].configure(text=f"{label} must be an integer.")
            return False
        if validation_type == 'float' and not re.match(self.patterns['float'], value):
            message_labels[label].configure(text=f"{label} must be a float (contain decimal point).")
            return False
        return True

