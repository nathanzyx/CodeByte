import customtkinter as ctk
from tkinter import messagebox

class LoginView:
    def __init__(self, parent, logic, inventory_system):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Login")
        self.window.geometry("500x500")
        self.logic = logic
        self.inventory_system = inventory_system
        self.setup_ui()
        
    def setup_ui(self):
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
               text="Login", 
               font=("Segoe UI", 14, "bold"),
               text_color="white").pack(padx=20, pady=15)
        
        # Main container
        main_container = ctk.CTkFrame(self.window, fg_color=colors['bg'], corner_radius=0)
        main_container.pack(fill=ctk.BOTH, expand=True, padx=40, pady=30)

        ctk.CTkLabel(main_container, text="Username is '123', Password is '123'", font=("Segoe UI", 12), text_color=colors['text']).pack(anchor="w", pady=(10, 5))

        # Username label
        ctk.CTkLabel(main_container, text="Username", font=("Segoe UI", 12), text_color=colors['text']).pack(anchor="w", pady=(10, 5))
        self.username_entry = ctk.CTkEntry(main_container, font=("Segoe UI", 12), width=200)
        self.username_entry.pack(pady=(0, 20))

        # Password label
        ctk.CTkLabel(main_container, text="Password", font=("Segoe UI", 12), text_color=colors['text']).pack(anchor="w", pady=(10, 5))
        self.password_entry = ctk.CTkEntry(main_container, font=("Segoe UI", 12), width=200, show="*")
        self.password_entry.pack(pady=(0, 20))

        # Login button
        login_button = ctk.CTkButton(main_container, text="Login", font=("Segoe UI", 12), fg_color=colors['primary'], text_color="white", command=self.authenticate_user)
        login_button.pack(pady=(10, 0))

    def authenticate_user(self):
        # Check if the username and password match the hardcoded values
        if self.username_entry.get() == self.inventory_system.username and self.password_entry.get() == self.inventory_system.password:
            self.inventory_system.logged_in = True
            
            messagebox.showinfo("Login Successful", "Welcome!")
            # LOG MESSAGE
            self.inventory_system.log_message(f" -- LOGIN SUCCESS: username: {str(self.inventory_system.username)}")
            self.crnt_user = self.username_entry.get()
            
            self.window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            # LOG MESSAGE
            self.inventory_system.log_message(f" -- LOGIN FAILED: attempted username: {str(self.username_entry.get())}, attempted password: {str(self.password_entry.get())}")
