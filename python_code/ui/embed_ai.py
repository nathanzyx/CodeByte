import tkinter as tk
from tkinter import ttk, Frame, Text, Scrollbar

#
# Embed Inventory Table Class is initialized with a function that returns a dataframe
# This class is embeds a table in a UI window
#
class EmbedAI:
    def __init__(self, llama, parent, modify_callback = None):
        self.llama = llama
        self.llama_frame = parent
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
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create header frame inside the parent
        header_frame = Frame(self.llama_frame, bg=self.colors['primary'], padx=20, pady=15)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(header_frame, text="Database Assistant", font=("Segoe UI", 15, "bold"), bg=self.colors['primary'], fg="white")
        header_label.pack(anchor="w")
        
        # Main container for the chat (This holds the Chat, The text box, and the send button)
        container = Frame(self.llama_frame, bg="white", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Message entry frame
        message_frame = Frame(container, bg=self.colors["bg"], relief="flat")
        message_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.message_entry = tk.Entry(message_frame, font=("Segoe UI", 12), width=50)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        submit_button = tk.Button(message_frame, text="Send", command=self.submit_message, font=("Segoe UI", 12), relief="flat", bg=self.colors['primary'], fg="white")
        submit_button.pack(side=tk.RIGHT)

        # Chat history text widget
        self.chat_history = Text(container, wrap=tk.WORD, state=tk.DISABLED, bg=self.colors['light_bg'], fg=self.colors['text'], relief="flat", font=("Segoe UI", 12))
        self.chat_history.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        self.chat_history.config(height=15)  # This sets a fixed height for the chat history
        
    def submit_message(self):
        user_message = self.message_entry.get()
        if user_message.strip():
            self.update_chat("User", user_message)
            self.message_entry.delete(0, tk.END)
            
            # Get AI's response
            ai_response = self.llama.make_Query(user_message)
            self.update_chat("AI", ai_response)
        
    def update_chat(self, sender, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{sender}: {message}\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    #     if selected_item:
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
