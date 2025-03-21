import tkinter as tk
from tkinter import messagebox, Frame

class LoginView:
    def __init__(self, parent, logic, inventory_system):
        self.window = tk.Toplevel(parent)
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
        header = Frame(self.window, bg=colors['warning'], pady=15)
        header.pack(fill=tk.X)
        
        tk.Label(header, 
               text="Login", 
               font=("Segoe UI", 14, "bold"),
               bg=colors['warning'],
               fg="white").pack(padx=20)
        
        # Main container
        main_container = Frame(self.window, bg=colors['bg'], padx=40, pady=30)
        main_container.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_container, text="Username is '123', Password is '123'", font=("Segoe UI", 12), bg=colors['bg'], fg=colors['text']).pack(anchor="w", pady=(10, 5))

        # Username label
        tk.Label(main_container, text="Username", font=("Segoe UI", 12), bg=colors['bg'], fg=colors['text']).pack(anchor="w", pady=(10, 5))
        self.username_entry = tk.Entry(main_container, font=("Segoe UI", 12), width=30)
        self.username_entry.pack(pady=(0, 20))

        # Password label
        tk.Label(main_container, text="Password", font=("Segoe UI", 12), bg=colors['bg'], fg=colors['text']).pack(anchor="w", pady=(10, 5))
        self.password_entry = tk.Entry(main_container, font=("Segoe UI", 12), width=30, show="*")
        self.password_entry.pack(pady=(0, 20))

        # Login button
        login_button = tk.Button(main_container, text="Login", font=("Segoe UI", 12), bg=colors['primary'], fg="white", command=self.authenticate_user)
        login_button.pack(pady=(10, 0))

    def authenticate_user(self):
        # Check if the username and password match the hardcoded values
        if self.username_entry.get() == self.inventory_system.username and self.password_entry.get() == self.inventory_system.password:
            self.inventory_system.logged_in = True
            self.window.destroy()
            messagebox.showinfo("Login Sucessfull", "Welcome!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
        