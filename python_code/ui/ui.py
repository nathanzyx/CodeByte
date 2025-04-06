import pandas as pd
import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QFrame, QMessageBox, QStackedWidget, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
import re
from ui.ui_logic import UILogic
# Remove the import for SearchViewEdit
# from ui.search_view_edit import SearchViewEdit
from ui.login_view import LoginView
from ui.add_item_view import AddItemView
from ui.remove_item_view import RemoveItemView
from ui.manage_fields_view import ManageFieldsView
from ui.activity_view import ActivityView
from PyQt6.QtWidgets import QPushButton, QMessageBox

from ui.embed_ai import EmbedAI
from ai.AI import AI 
from ui.inventory_view import InventoryView  # Import the new InventoryView

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
        self.app = QApplication(sys.argv)
        self.root = QMainWindow()
        
        self.colors = {
            'bg': '1e1e1e',
            'sidebar': '#ffffff',
            'primary': '#363062',
            'secondary': '#424242',
            'accent': '#2196f3',
            'danger': '#f44336',
            'text': '#2c3e50',
            'subtext': '#c01fed'
        }
        self.container = None
        self.content = None
        self.ai_frame = None

        # Initialize QStackedWidget
        self.stacked_widget = QStackedWidget()
        
        # Create default view with original dashboard theme
        self.default_view = QWidget()
        default_layout = QVBoxLayout(self.default_view)
        default_layout.setContentsMargins(20, 20, 20, 20)  # Add some padding
        
        # Set the background color for the default view
        self.default_view.setStyleSheet("background-color: #1e1e1e;")  # Darker background
        
        # Fix welcome frame stylesheet
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 12px;
                border: 1px solid #374151;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Create and set up background frame for default view
        # Fix background frame stylesheet
        background_frame = QFrame(self.default_view)
        background_frame.setStyleSheet("background-color: #1e1e1e;")
        background_frame.setGeometry(0, 0, self.default_view.width(), self.default_view.height())
        background_frame.setAutoFillBackground(True)
        
        # Fix welcome frame stylesheet
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 12px;
                border: 1px solid #374151;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Fix stats container stylesheet
        stats_container = QFrame()
        stats_container.setStyleSheet("background-color: #1e1e1e;")
        
        # Fix AI frame stylesheet
        self.ai_frame = QFrame()
        self.ai_frame.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 12px;
                border: 1px solid #374151;
            }
            QLabel {
                color: #E5E7EB;
            }
            QTextEdit {
                background-color: #111827;
                border: 1px solid #374151;
                border-radius: 8px;
                color: #E5E7EB;
                padding: 8px;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        
        # Fix sidebar stylesheet
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            background-color: #16181A;
        """)
        
        # Fix profile frame stylesheet
        profile_frame = QFrame()
        profile_frame.setStyleSheet("""
            QFrame {
                background-color: #313538;
                border-radius: 8px;
                margin-bottom: 8px;
            }
        """)
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setContentsMargins(20, 20, 20, 20)
        
        welcome_title = QLabel("Welcome to Your Inventory Dashboard")
        welcome_title.setFont(QFont("Inter", 20, QFont.Weight.Bold))
        welcome_title.setStyleSheet("color: #F9FAFB; background: transparent;")
        welcome_layout.addWidget(welcome_title)
        
        welcome_subtitle = QLabel("Manage your inventory efficiently with our modern interface")
        welcome_subtitle.setFont(QFont("Inter", 12))
        welcome_subtitle.setStyleSheet("color: #9CA3AF; background: transparent;")
        welcome_layout.addWidget(welcome_subtitle)

        default_layout.addWidget(welcome_frame)

        # Stats cards container
        stats_container = QFrame()
        stats_container.setStyleSheet("background-color: #1e1e1e;")
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(0, 20, 0, 20)

        def create_stat_card(title, value, icon, show_settings=False):
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #1F2937;
                    border-radius: 12px;
                    border: none;
                }
                QLabel {
                    background-color: transparent;
                    border: none;
                }
                QLineEdit {
                    background-color: #374151;
                    color: #E5E7EB;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    max-width: 60px;
                }
                QLineEdit:focus {
                    border-color: #3B82F6;
                }
            """)
            
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 15, 20, 15)
            
            # Create a container frame for the content
            content_container = QFrame()
            container_layout = QVBoxLayout(content_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            
            # Icon and content
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Inter", 24))
            icon_label.setStyleSheet("color: #E5E7EB;")
            container_layout.addWidget(icon_label)
            
            title_label = QLabel(title)
            title_label.setFont(QFont("Inter", 11))
            title_label.setStyleSheet("color: #9CA3AF;")
            container_layout.addWidget(title_label)
            
            value_label = QLabel(value)
            value_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))
            value_label.setStyleSheet("color: #F9FAFB;")
            container_layout.addWidget(value_label)
            
            card_layout.addWidget(content_container)
            
            # Add floating input if show_settings is True
            if show_settings:
                threshold_input = QLineEdit(card)
                threshold_input.setPlaceholderText("Qty")
                threshold_input.setFixedSize(60, 28)
                threshold_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
                threshold_input.setStyleSheet("""
                    QLineEdit {
                        background-color: #374151;
                        color: #E5E7EB;
                        border: 1px solid #4B5563;
                        border-radius: 4px;
                        padding: 4px 8px;
                    }
                    QLineEdit:focus {
                        border-color: #3B82F6;
                    }
                """)
                
                def update_low_stock_count():
                    try:
                        threshold = int(threshold_input.text())
                        items_df = self.inventory_system.get_all_items()
                        if 'quantity' in items_df.columns:
                            low_stock_count = len(items_df[items_df['quantity'].astype(float) <= threshold])
                            value_label.setText(str(low_stock_count))
                    except ValueError:
                        value_label.setText("--")
                
                threshold_input.textChanged.connect(update_low_stock_count)
                threshold_input.move(card.width() - 80, 15)  # Position in top-right corner
                
                # Handle card resize to keep input in correct position
                def on_resize():
                    threshold_input.move(card.width() - 80, 15)
                
                card.resizeEvent = lambda e: on_resize()
            
            return card
        
        def calculate_total_value():
            items_df = self.inventory_system.get_all_items()
            if 'price' in items_df.columns and 'quantity' in items_df.columns:
                # Convert price to float and multiply by quantity
                items_df['price'] = items_df['price'].astype(float)
                items_df['quantity'] = items_df['quantity'].astype(float)
                total_value = (items_df['price'] * items_df['quantity']).sum()
                return f"${total_value:,.2f}"
            return "$0.00"

        # Add stats cards with real data
        stats_layout.addWidget(create_stat_card("Total Products", str(len(self.inventory_system.get_all_items())), "📦"))
        stats_layout.addWidget(create_stat_card("Low Stock Items", "--", "⚠️", show_settings=True))
        stats_layout.addWidget(create_stat_card("Total Value", calculate_total_value(), "💰"))
        
        default_layout.addWidget(stats_container)
        
        # AI Assistant section
        self.ai_frame = QFrame()
        self.ai_frame.setStyleSheet("background-color: #1F2937; border-radius: 12px;")
        self.embed_ai = EmbedAI(self.ai, self.ai_frame)  # Pass the AI instance
        default_layout.addWidget(self.ai_frame)
        
        # Remove or comment out this line as it creates a duplicate instance
        # EmbedAI(self.ai, self.ai_frame)
        self.ai_frame.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 12px;
                border: 1px solid #374151;
            }
            QLabel {
                color: #E5E7EB;
            }
            QTextEdit {
                background-color: #111827;
                border: 1px solid #374151;
                border-radius: 8px;
                color: #E5E7EB;
                padding: 8px;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        default_layout.addWidget(self.ai_frame, 1)  # 1 is the stretch factor
        
        # Initialize AI assistant
        EmbedAI(self.ai, self.ai_frame)
        
        # Footer
        footer = QFrame()
        footer.setStyleSheet(f"background-color: {self.colors['bg']};")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 10, 0, 0)
        
        current_time = datetime.now().strftime("%d %b %Y")
        version_label = QLabel(f"v1.0 • {current_time}")
        version_label.setFont(QFont("Inter", 9))
        version_label.setStyleSheet(f"color: {self.colors['subtext']};")
        footer_layout.addStretch()
        footer_layout.addWidget(version_label)
        
        default_layout.addWidget(footer)
        
        # Add default view and inventory view to QStackedWidget
        self.stacked_widget.addWidget(self.default_view)
        self.inventory_view = InventoryView(self.root, self.inventory_system, self.ai)  # Use the new InventoryView
        self.stacked_widget.addWidget(self.inventory_view)
        
        # Create add product view and add it to stacked widget
        from ui.add_item_view import AddItemView
        self.add_product_view = QWidget()
        add_product_layout = QVBoxLayout(self.add_product_view)
        add_product_layout.setContentsMargins(0, 0, 0, 0)
        self.add_item_view = AddItemView(self.root, self.logic, self.inventory_system)
        add_product_layout.addWidget(self.add_item_view)
        self.stacked_widget.addWidget(self.add_product_view)

        # Create remove product view and add it to stacked widget
        self.remove_product_view = QWidget()
        remove_product_layout = QVBoxLayout(self.remove_product_view)
        remove_product_layout.setContentsMargins(0, 0, 0, 0)
        self.remove_item_view = RemoveItemView(self.root, self.inventory_system, self.patterns)
        remove_product_layout.addWidget(self.remove_item_view)
        self.stacked_widget.addWidget(self.remove_product_view)
        
        # Create the activity view and add it to the stacked widget
        from ui.activity_view import ActivityView
        self.activity_view = QWidget()
        activity_layout = QVBoxLayout(self.activity_view)
        activity_layout.setContentsMargins(0, 0, 0, 0)
        self.activity_view_instance = ActivityView(self.root, self.logic, self.inventory_system)
        activity_layout.addWidget(self.activity_view_instance)
        self.stacked_widget.addWidget(self.activity_view)
    
    #
    #   This function returns the users login status along with a message if not logged in
    #
    def is_authenticated(self):
        if self.inventory_system.logged_in or not self.inventory_system.login_required():
            return True
        QMessageBox.critical(self.root, "Login Required", "You must be logged in to perform this action.")
        return False
        
    def display_inventory(self):
        if not self.is_authenticated():
            return
        # Switch to the inventory view in the stacked widget
        self.stacked_widget.setCurrentWidget(self.inventory_view)
        # Refresh the inventory view to show the latest data
        self.inventory_view.display_all_items()
        self.refresh_views()
        
    def display_activity(self):
        if not self.is_authenticated():
            return
        # Switch to the activity view in the stacked widget
        self.stacked_widget.setCurrentWidget(self.activity_view)
        # Refresh the view to show the latest activity data
        if hasattr(self, 'activity_view'):
            # Recreate the activity view to reflect any changes
            self.stacked_widget.removeWidget(self.activity_view)
            self.activity_view = ActivityView(self.root, self.logic, self.inventory_system)
            self.stacked_widget.addWidget(self.activity_view)
            self.stacked_widget.setCurrentWidget(self.activity_view)
    
    def display_add_item(self):
        if not self.is_authenticated():
            return
        # Switch to the add product view in the stacked widget
        self.stacked_widget.setCurrentWidget(self.add_product_view)
        # Refresh the view to show the latest fields
        if hasattr(self, 'add_product_view'):
            # Recreate the add item view to reflect any field changes
            self.stacked_widget.removeWidget(self.add_product_view)
            self.add_product_view = AddItemView(self.root, self.logic, self.inventory_system)
            self.stacked_widget.addWidget(self.add_product_view)
            self.stacked_widget.setCurrentWidget(self.add_product_view)
    
    def display_remove_item(self):
        if not self.is_authenticated():
            return
        # Switch to the remove product view in the stacked widget
        self.stacked_widget.setCurrentWidget(self.remove_product_view)
        # Refresh the view to show the latest items
        if hasattr(self, 'remove_product_view'):
            # Check if the method exists before calling it
            if hasattr(self.remove_product_view, 'refresh_items'):
                self.remove_product_view.refresh_items()
            else:
                print("Warning: remove_product_view does not have refresh_items method")
                # Recreate the remove item view to reflect any changes
                index = self.stacked_widget.indexOf(self.remove_product_view)
                self.stacked_widget.removeWidget(self.remove_product_view)
                
                # Import here to avoid circular imports
                from ui.remove_item_view import RemoveItemView
                self.remove_product_view = RemoveItemView(self.root, self.inventory_system, self.patterns)
                
                self.stacked_widget.insertWidget(index, self.remove_product_view)
                self.stacked_widget.setCurrentWidget(self.remove_product_view)
    
    def display_options(self):
        if not self.is_authenticated():
            return
        # Create the manage fields view and add it to the stacked widget if it doesn't exist
        if not hasattr(self, 'manage_fields_view'):
            self.manage_fields_view = ManageFieldsView(self.root, self.logic, self.inventory_system)
            self.stacked_widget.addWidget(self.manage_fields_view)
        # Switch to the manage fields view
        self.stacked_widget.setCurrentWidget(self.manage_fields_view)
    
    def display_login(self):
        
        login_dialog = LoginView(self.root, self.logic, self.inventory_system)
        login_dialog.exec()
            
        # Refresh the menu after successful login
        if self.inventory_system.logged_in:
            self.crnt_user = self.inventory_system.username  # Update current user
            # Store current window size
            current_size = self.root.size()
            # Clear and rebuild the menu
            if self.root.centralWidget():
                self.root.centralWidget().deleteLater()
            self.display_menu()
            # Restore the window size
            self.root.resize(current_size)
                
            # Add this to refresh the AI chat interface
            if hasattr(self, 'embed_ai'):
                self.embed_ai.update_login_state()
    
    def display_ai_assistant(self):
        # Remove this method or modify it to avoid adding a layout twice
        # The EmbedAI is already being called in display_menu
        pass
    
    def display_clear_database(self):
        if not self.is_authenticated():
            return
        self.inventory_system.clear_database()
        
    def exit_application(self):
        # Perform any actions you want before exiting
        print("Closing App...")
        self.inventory_system.log_message(f" LOGOUT: user:{str(self.crnt_user)}")

        # Exit application
        self.app.quit()
        
    #   MENU
    #       - Display Inventory (see all products in database table)
    #       - Add/Remove Product
    #       - Options (add or remove field)
    #       - Clear Database (for testing)
    #       - Exit (quit the program)
    def display_menu(self):
        # Configure the main window
        self.root.setWindowTitle(self.inventory_system.name)
        
        # Replace the fixed size with minimum size
        self.root.setMinimumSize(1200, 800)  # Set minimum size based on the warning message
        self.root.resize(1200, 800)  # Initial size, but now resizable
        
        # Create central widget
        central_widget = QWidget()
        self.root.setCentralWidget(central_widget)
        
        # Create main container with sidebar and content area
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create a dark background for the entire dashboard
        dashboard_background = QFrame()
        dashboard_background.setStyleSheet("background-color: #1e1e1e;")  # Darker background
        dashboard_background.setAutoFillBackground(True)
        dashboard_background.lower()  # Move to the back
        
        # Create sidebar with dark mode
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #16181A;")
        sidebar.setFixedWidth(260)  # Reduced width to match NextUI
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)  # Match NextUI padding
        sidebar_layout.setSpacing(0)
        
        # Header with logo
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_frame.setFixedHeight(50)  # Reduced height
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 16)  # Bottom margin only
        
        # Cool app logo with emojis
        app_logo = QLabel("🚀 Electronics")
        app_logo.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        app_logo.setStyleSheet("""
            color: #ECEDEE;
            padding: 8px 4px;
        """)
        
        # Add a status indicator - green dot
        status_indicator = QLabel("●")
        status_indicator.setFont(QFont("Inter", 8))
        status_indicator.setStyleSheet("""
            color: #17C964;  /* Green dot */
            margin-left: 8px;
            padding-bottom: 2px;
        """)
        
        # Add a version label
        version_indicator = QLabel("v1.0")
        version_indicator.setFont(QFont("Inter", 8))
        version_indicator.setStyleSheet("""
            color: #889096;
            margin-left: 12px;
            background-color: #2D3135;
            padding: 2px 6px;
            border-radius: 4px;
        """)
        
        header_layout.addWidget(app_logo)
        header_layout.addWidget(status_indicator)
        header_layout.addWidget(version_indicator)
        header_layout.addStretch()  # Push everything to the left
        
        sidebar_layout.addWidget(header_frame)
        
        # Add a subtle horizontal separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #313538; max-height: 1px;")
        sidebar_layout.addWidget(separator)
        sidebar_layout.addSpacing(8)  # Add a bit of space after the separator
        
        # Sidebar body
        body_frame = QFrame()
        body_frame.setStyleSheet("background-color: transparent;")
        body_layout = QVBoxLayout(body_frame)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(4)  # Reduced spacing between items
        
        # NextUI sidebar item style for dark mode
        sidebar_item_style = """
            QPushButton {
                background-color: transparent;
                color: #7E868C;
                border: none;
                text-align: left;
                padding: 6px 12px;
                font-family: 'Inter';
                font-size: 10pt;
                border-radius: 6px;
                min-height: 34px;
            }
            QPushButton:hover {
                background-color: #313538;
            }
            QPushButton:checked {
                background-color: rgba(0, 111, 238, 0.15);
                color: #006FEE;
                font-weight: 500;
            }
        """
        
        # After the sidebar_item_style definition, add this:
        self.sidebar_buttons = []  # Store all sidebar buttons
        
        # Modify the create_sidebar_item function:
        def create_sidebar_item(text, icon, command, is_active=False):
            btn = QPushButton(f" {icon}  {text}")
            btn.setFont(QFont("Inter", 9))
            btn.setStyleSheet(sidebar_item_style)
            btn.setCheckable(True)
            btn.setChecked(is_active)
            
            # Create a wrapped command that handles button states
            def wrapped_command():
                # Uncheck all other buttons
                for other_btn in self.sidebar_buttons:
                    other_btn.setChecked(False)
                btn.setChecked(True)
                command()
            
            btn.clicked.connect(wrapped_command)
            self.sidebar_buttons.append(btn)  # Add button to the group
            return btn

        # Create sidebar items as before
        def wrapped_command_for_home():
            # Uncheck all other buttons
            for other_btn in self.sidebar_buttons:
                other_btn.setChecked(False)
            home_btn.setChecked(True)
            self.stacked_widget.setCurrentWidget(self.default_view)
            # Refresh the dashboard stats
            self.refresh_dashboard_stats()

        home_btn = create_sidebar_item("Dashboard", "🏠", wrapped_command_for_home, True)
        body_layout.addWidget(home_btn)
        
        # Add spacing
        body_layout.addSpacing(16)
        
        # Main Menu section
        menu_label = QLabel("MAIN MENU")
        menu_label.setFont(QFont("Inter", 9))
        menu_label.setStyleSheet("color: #7E868C; margin-bottom: 4px; letter-spacing: 0.04em;")
        body_layout.addWidget(menu_label)
        
        # Main menu items
        body_layout.addWidget(create_sidebar_item("Inventory", "📊", self.display_inventory))  # Update to use display_inventory
        # Create sidebar item for Add Product
        add_product_btn = create_sidebar_item("Add Product", "➕", self.display_add_item, is_active=False)
        body_layout.addWidget(add_product_btn)
        # Create sidebar item for Remove Product
        remove_product_btn = create_sidebar_item("Remove Product", "➖", self.display_remove_item, is_active=False)
        body_layout.addWidget(remove_product_btn)
        # Activity
        display_activity_btn = create_sidebar_item("Activity", "⏱️", self.display_activity, is_active=False)
        body_layout.addWidget(display_activity_btn)
        
        # Add spacing
        body_layout.addSpacing(16)
        
        # Settings section
        settings_label = QLabel("SETTINGS")
        settings_label.setFont(QFont("Inter", 9))
        settings_label.setStyleSheet("color: #7E868C; margin-bottom: 4px; letter-spacing: 0.04em;")
        body_layout.addWidget(settings_label)
        
        # Settings items
        # Add the Manage Fields button
        body_layout.addWidget(create_sidebar_item("Manage Fields", "🔧", self.display_options))
        
        # Remove the duplicate Clear Database buttons and use only one Clear All Data button
        body_layout.addWidget(create_sidebar_item("Clear Database", "🗑️", self.display_clear_database))
        
        body_layout.addStretch()
        
        # Footer section with login and exit
        footer_frame = QFrame()
        footer_frame.setStyleSheet("background-color: transparent;")
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(8)
        
        # User profile section
        if self.inventory_system.logged_in:
            profile_frame = QFrame()
            profile_frame.setStyleSheet("""
                QFrame {
                    background-color: #313538;
                    border-radius: 8px;
                    margin-bottom: 8px;
                }
            """)
            profile_layout = QHBoxLayout(profile_frame)
            profile_layout.setContentsMargins(12, 8, 12, 8)
            
            # User avatar circle
            avatar_label = QLabel("👤")
            avatar_label.setStyleSheet("""
                QLabel {
                    background-color: #006FEE;
                    color: white;
                    border-radius: 15px;
                    padding: 5px;
                    min-width: 30px;
                    min-height: 30px;
                }
            """)
            avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Username and role
            user_info_layout = QVBoxLayout()
            user_info_layout.setSpacing(0)
            
            username_label = QLabel(str(self.crnt_user))
            username_label.setFont(QFont("Inter", 9, QFont.Weight.Bold))
            username_label.setStyleSheet("color: #ECEDEE;")
            
            role_label = QLabel("Admin")
            role_label.setFont(QFont("Inter", 8))
            role_label.setStyleSheet("color: #7E868C;")
            
            user_info_layout.addWidget(username_label)
            user_info_layout.addWidget(role_label)
            
            profile_layout.addWidget(avatar_label)
            profile_layout.addLayout(user_info_layout)
            profile_layout.addStretch()
            
            # Online status indicator
            status_label = QLabel("●")
            status_label.setStyleSheet("color: #17C964;")  # Green dot for online status
            profile_layout.addWidget(status_label)
            
            edit_btn = QPushButton("Profile")
            edit_btn.setFont(QFont("Inter", 9))
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #006FEE;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #0057CC;
                }
            """)
            edit_btn.clicked.connect(self.display_login)
            profile_layout.addWidget(edit_btn)
            
            footer_layout.addWidget(profile_frame)
        else:
            # Login button (show only if not logged in)
            login_btn = QPushButton(" ✅  Login")
            login_btn.setFont(QFont("Inter", 10))
            login_btn.setStyleSheet("""
                QPushButton {
                    background-color: #006FEE;
                    color: white;
                    border: none;
                    text-align: left;
                    padding: 8px 16px;
                    border-radius: 8px;
                    min-height: 38px;
                }
                QPushButton:hover {
                    background-color: #0057CC;
                }
            """)
            login_btn.clicked.connect(self.display_login)
            footer_layout.addWidget(login_btn)
        
        # Exit button
        exit_btn = QPushButton(" 🚪  Exit Application")
        exit_btn.setFont(QFont("Inter", 10))
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #F31260;
                color: white;
                border: none;
                text-align: left;
                padding: 8px 16px;
                border-radius: 8px;
                min-height: 38px;
                margin-top: 4px;
            }
            QPushButton:hover {
                background-color: #C50F50;
            }
        """)
        exit_btn.clicked.connect(self.exit_application)
        
        footer_layout.addWidget(exit_btn)
        
        # Add watermark
        watermark = QLabel("Made by CodeByte")
        watermark.setFont(QFont("Inter", 8, QFont.Weight.Normal, True))  # Italic
        watermark.setStyleSheet("color: #7E868C; margin-top: 8px;")
        watermark.setAlignment(Qt.AlignmentFlag.AlignRight)
        footer_layout.addWidget(watermark)
        
        sidebar_layout.addWidget(body_frame, 1)  # 1 is stretch factor
        sidebar_layout.addWidget(footer_frame)
        
        # Add sidebar and QStackedWidget to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget, 1)  # 1 is stretch factor

        # Check if help button already exists before adding a new one
        help_button_exists = False
        for widget in self.root.statusBar().findChildren(QPushButton):
            if widget.text() == "❓ Help":
                help_button_exists = True
                break
                
        if not help_button_exists:
            # Create a help button in the status bar (always visible)
            self.root.statusBar().setStyleSheet("""
                QStatusBar {
                    background-color: #1e1e1e;
                    color: #E5E7EB;
                    border-top: 1px solid #374151;
                }
            """)
            
            help_button = QPushButton("❓ Help")
            help_button.setFont(QFont("Inter", 9))
            help_button.setStyleSheet("""
                QPushButton {
                    background-color: #3B82F6;
                    color: white;
                    border-radius: 4px;
                    padding: 4px 10px;
                    margin: 2px 5px;
                }
                QPushButton:hover {
                    background-color: #2563EB;
                }
            """)
            help_button.clicked.connect(self.show_help)
            self.root.statusBar().addPermanentWidget(help_button)

        # Show the main window
        self.root.show()
        
    def run(self):
        # Start the application
        sys.exit(self.app.exec())

    def validate_input(self, value, validation_type, is_required, label, message_labels):
        if is_required and not value.strip():
            message_labels[label].setText(f"{label} is required.")
            return False
        if not is_required and not value.strip():
            return True
        if validation_type == 'string' and not re.match(self.patterns['string'], value):
            message_labels[label].setText(f"{label} contains invalid characters.")
            return False
        if validation_type == 'int' and not re.match(self.patterns['int'], value):
            message_labels[label].setText(f"{label} must be an integer.")
            return False
        if validation_type == 'float' and not re.match(self.patterns['float'], value):
            message_labels[label].setText(f"{label} must be a float (contain decimal point).")
            return False
        return True

    def refresh_views(self):
        """Refresh all views to reflect database changes"""
        # Refresh inventory view
        if hasattr(self, 'inventory_view'):
            self.inventory_view.display_all_items()
        
        # Refresh manage fields view
        if hasattr(self, 'manage_fields_view'):
            self.manage_fields_view.refresh_fields()
        
        # Refresh add item view by recreating it
        if hasattr(self, 'add_product_view') and self.stacked_widget.currentWidget() == self.add_product_view:
            index = self.stacked_widget.indexOf(self.add_product_view)
            self.stacked_widget.removeWidget(self.add_product_view)
            self.add_product_view = AddItemView(self.root, self.logic, self.inventory_system)
            self.stacked_widget.insertWidget(index, self.add_product_view)
            self.stacked_widget.setCurrentWidget(self.add_product_view)
        
        # Refresh remove item view
        if hasattr(self, 'remove_product_view'):
            # Assuming there's a refresh_items method in RemoveItemView
            if hasattr(self.remove_product_view, 'refresh_items'):
                self.remove_product_view.refresh_items()

    # Add this function to your UI class to refresh dashboard statistics
    def refresh_dashboard_stats(self):
        # Find the stats container in the default view
        stats_container = None
        for i in range(self.default_view.layout().count()):
            item = self.default_view.layout().itemAt(i)
            if item.widget() and isinstance(item.widget(), QFrame):
                if item.widget().layout() and isinstance(item.widget().layout(), QHBoxLayout):
                    stats_container = item.widget()
                    break
                    
        if not stats_container:
            return
            
        # Update total products count
        product_count = len(self.inventory_system.get_all_items())
        stats_layout = stats_container.layout()
        if stats_layout.count() > 0:
            product_card = stats_layout.itemAt(0).widget()
            for i in range(product_card.layout().count()):
                content = product_card.layout().itemAt(i).widget()
                if isinstance(content, QFrame):
                    for j in range(content.layout().count()):
                        widget = content.layout().itemAt(j).widget()
                        if isinstance(widget, QLabel) and widget.font().pointSize() == 20:
                            widget.setText(str(product_count))
                            break
        
        # Update total value
        total_value = self.calculate_total_value()
        if stats_layout.count() > 2:
            value_card = stats_layout.itemAt(2).widget()
            for i in range(value_card.layout().count()):
                content = value_card.layout().itemAt(i).widget()
                if isinstance(content, QFrame):
                    for j in range(content.layout().count()):
                        widget = content.layout().itemAt(j).widget()
                        if isinstance(widget, QLabel) and widget.font().pointSize() == 20:
                            widget.setText(total_value)
                            break

    # Move calculate_total_value out of the display_menu method and make it a class method
    def calculate_total_value(self):
        items_df = self.inventory_system.get_all_items()
        if 'price' in items_df.columns and 'quantity' in items_df.columns:
            # Convert price to float and multiply by quantity
            items_df['price'] = items_df['price'].astype(float)
            items_df['quantity'] = items_df['quantity'].astype(float)
            total_value = (items_df['price'] * items_df['quantity']).sum()
            return f"${total_value:,.2f}"
        return "$0.00"

    def show_help(self):
        """Display help information"""
        help_dialog = QMessageBox(self.root)
        help_dialog.setWindowTitle("Help")
        help_dialog.setIcon(QMessageBox.Icon.Information)
        help_dialog.setText("Electronics Inventory Management Help")
        
        help_text = """
        <h3>Quick Help Guide:</h3>
        <ul>
            <li><b>Dashboard:</b> Inventory Statistics and AI Assistant</li>
            <li><b>Inventory:</b> Browse and Search all Items</li>
            <li><b>Add Product:</b> Add New Items to Inventory</li>
            <li><b>Remove Product:</b> Remove Items from the Inventory</li>
            <li><b>Activity:</b> See the Timeline of Database Operations</li>
            <li><b>Manage Fields:</b> Customize database Fields</li>
            <li><b>Clear Database:</b> Erase Inventory and Custom Fields</li>
            <li><b>Profile (When Logged In):</b> Change Profile/System Options</li>
        </ul>
        """
        
        help_dialog.setInformativeText(help_text)
        help_dialog.exec()

