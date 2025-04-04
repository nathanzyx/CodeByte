from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTextEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor

#
# Embed AI Class is initialized with a llama instance and a parent frame
# This class embeds an AI chat interface in a UI window
#
class EmbedAI:
    def __init__(self, llama, parent, modify_callback = None):
        self.llama = llama
        self.llama_frame = parent
        self.modify_callback = modify_callback
        
        self.colors = {
            'primary': '#1F2937',      # Dark background
            'secondary': '#374151',    # Slightly lighter background
            'accent': '#3B82F6',       # Blue accent
            'user_bg': '#251e45',      # Darker blue for user messages
            'ai_bg': '#1F2937',        # Dark gray for AI messages
            'text': '#F9FAFB',         # Light text
            'subtext': '#9CA3AF',      # Lighter text
            'border': '#374151',       # Border color
            'input_bg': '#111827'      # Dark input background
        }
        
        self.setup_ui()

    # Modify this method to always enable the chat
    def update_login_state(self):
        """Update the input field state to always be enabled"""
        # Always enable the chat input regardless of login status
        self.message_entry.setEnabled(True)
        self.message_entry.setPlaceholderText("Type your message here...")

    def setup_ui(self):
        # Create main layout for the parent frame
        main_layout = QVBoxLayout(self.llama_frame)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Create header frame inside the parent
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary']};
                border-radius: 8px;
                border: 1px solid {self.colors['border']};
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        header_label = QLabel("Database Assistant")
        header_label.setStyleSheet(f"color: {self.colors['text']};")
        header_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        header_layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignLeft)
        
        main_layout.addWidget(header_frame)
        
        # Main container for the chat
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary']};
                border-radius: 8px;
                border: 1px solid {self.colors['border']};
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        
        # Chat history text widget
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.colors['input_bg']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 0px;
            }}
        """)
        self.chat_history.setFont(QFont("Inter", 12))
        self.chat_history.setFixedHeight(210)
        container_layout.addWidget(self.chat_history)
        
        # Message entry frame
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        message_layout = QHBoxLayout(message_frame)
        message_layout.setContentsMargins(0, 8, 0, 0)  # Adjusted top margin to 8px
        message_layout.setSpacing(10)
        
        self.message_entry = QLineEdit()
        self.message_entry.setFont(QFont("Inter", 12))
        # Always enable the input regardless of login status
        self.message_entry.setEnabled(True)
        self.message_entry.setPlaceholderText("Type your message here...")
        self.message_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['input_bg']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 8px;
                padding: 8px 12px;
            }}
            QLineEdit:disabled {{
                opacity: 0.6;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
            }}
        """)
        self.message_entry.returnPressed.connect(self.submit_message)
        message_layout.addWidget(self.message_entry)
        
        submit_button = QPushButton("Send")
        submit_button.setFont(QFont("Inter", 12))
        submit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: #2563EB;
            }}
        """)
        submit_button.clicked.connect(self.submit_message)
        message_layout.addWidget(submit_button)
        
        container_layout.addWidget(message_frame)
        main_layout.addWidget(container, 1)

    def submit_message(self):
        user_message = self.message_entry.text()
        if user_message.strip():
            # Clear input and show user message immediately
            self.message_entry.clear()
            self.update_chat("You", user_message)
            
            # Force the UI to update and show the user message
            QTimer.singleShot(100, lambda: self._process_ai_response(user_message))
            
    def _process_ai_response(self, user_message):
        # Store the current content
        current_content = self.chat_history.toHtml()
        
        # Show loading message
        self.update_chat("System", "Generating response...")
        
        try:
            # Get AI response
            ai_response = self.llama.make_Query(user_message)
            
            # Restore previous content (removing only loading message)
            self.chat_history.setHtml(current_content)
            
            # Show AI response
            self.update_chat("AI", ai_response)
        except Exception as e:
            # Restore previous content (removing only loading message)
            self.chat_history.setHtml(current_content)
            
            # Show error message
            self.update_chat("System", f"Error: {str(e)}")
            print(f"Query failed: {e}")

    def _remove_last_message(self):
        # Get the document
        document = self.chat_history.document()
        
        # Create a cursor at the end of the document
        cursor = document.rootFrame().lastCursorPosition()
        
        # Select the last block (message)
        cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.KeepAnchor)
        cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.KeepAnchor)
        cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.KeepAnchor)
        
        # Delete the selected text
        cursor.removeSelectedText()
        
    def update_chat(self, sender, message):
        # Create a cursor for text manipulation
        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Set text format based on sender
        format = QTextCharFormat()
        format.setFont(QFont("Inter", 12))
        
        if sender == "You":
            format.setForeground(QColor("#93C5FD"))  # Light blue for user name
            format.setBackground(QColor(self.colors['user_bg']))  # Dark blue background
        elif sender == "AI":
            format.setForeground(QColor("#10B981"))  # Emerald green for AI name
            format.setBackground(QColor(self.colors['ai_bg']))  # Dark gray background
        else:
            format.setForeground(QColor("#111827"))  # Dark text for system messages
            format.setBackground(QColor("#f59e0b"))  # Amber background
        
        # Insert sender name
        cursor.insertText(f"{sender}:\n", format)
        
        # Reset format for message
        message_format = QTextCharFormat()
        message_format.setFont(QFont("Inter", 12))
        message_format.setForeground(QColor(self.colors['text']))
        
        # Insert message
        cursor.insertText(f"{message}\n\n", message_format)
        
        # Scroll to the bottom
        self.chat_history.verticalScrollBar().setValue(
            self.chat_history.verticalScrollBar().maximum()
        )

            #     # Set modern style for the treeview
    #     style = ttk.Style()
    #     style.theme_use("clam")
        
    #     style.configure("Treeview", 
    #                     background=self.colors['bg'],
    #                     foreground="#212529",
    #                     rowheight=25,
    #                     fieldbackground=self.colors['bg'])
        
    #     # Create header frame inside the parent
    #     header_frame = Frame(self.parent, bg="#363062", padx=20, pady=15)
    #     header_frame.pack(fill=tk.X)
                
    #     # Main container for the table
    #     container = Frame(self.parent, bg="white", padx=20, pady=20)
    #     container.pack(fill=tk.BOTH, expand=True)
        
    #     # Create the treeview widget with the appropriate columns
    #     self.tree = ttk.Treeview(container, columns=self.columns, show="headings")
        
    #     # Columns for table format
    #     for col in self.columns:
    #         self.tree.heading(col, text=col.capitalize(), anchor='center')
    #         self.tree.column(col, anchor='center', width=100)
    #     # Rows for table format
    #     for row in self.rows:
    #         self.tree.insert("", "end", values=row)
            
    #     # Add Initial row colors
    #     self.tree.tag_configure('oddrow', background='#f8f9fa')
    #     self.tree.tag_configure('evenrow', background='#e9ecef')
    #     for i, item in enumerate(self.tree.get_children()):
    #         self.tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow',))
        
    #     # ENABLE SCROLLING
    #     y_scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
    #     x_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
    #     self.tree.configure(yscroll=y_scrollbar.set, xscroll=x_scrollbar.set)
    #     y_scrollbar.pack(side="right", fill="y")
    #     x_scrollbar.pack(side="bottom", fill="x")
    #     self.tree.pack(expand=True, fill="both")
        
    #     footer = Frame(self.parent, bg="#f0f2f5", padx=10, pady=5)
    #     footer.pack(fill=tk.X, side=tk.BOTTOM)
        
    #     watermark = tk.Label(footer, 
    #                          text="Made by CodeByte",
    #                          font=("Segoe UI", 8, "italic"),
    #                          fg="#a0a0a0",
    #                          bg="#f0f2f5")
    #     watermark.pack(side=tk.RIGHT)
        
    #     if self.modify_callback is not None:
    #         self.tree.bind("<Double-1>", lambda event: self.modify_callback(self.get_selected_item()))
    
    # def get_selected_item(self):
    #     selected_item = self.tree.focus()
    #     if (selected_item):
    #         return self.tree.item(selected_item)['values']
    #     return None
    
    # def update_table(self, new_df):
    #     self.df = new_df
    #     self.columns = self.df.columns.tolist()
    #     self.rows = self.df.values.tolist()

    #     # Clear existing items form the table
    #     for item in self.tree.get_children():
    #         self.tree.delete(item)
        
    #     # Add the new items from the search results
    #     for row in self.rows:
    #         self.tree.insert("", "end", values=row)

    #     # Reset the row colors
    #     for i, item in enumerate(self.tree.get_children()):
    #         self.tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow',))