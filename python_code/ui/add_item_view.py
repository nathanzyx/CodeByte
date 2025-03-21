import tkinter as tk
from tkinter import messagebox, Frame

class AddItemView:
    def __init__(self, parent, logic, inventory_system):
        self.window = tk.Toplevel(parent)
        self.window.title("Add Item")
        self.window.geometry("750x500")
        self.window.resizable(False, False)
        self.logic = logic
        self.inventory_system = inventory_system
        self.entries = {}
        self.message_labels = {}
        self.setup_ui()
        
    def setup_ui(self):
        # Get field specifications
        self.entries, self.message_labels, self.prod_specs = self.logic.get_add_item_specs(self.window)
        
        # Color palette
        colors = {
            'primary': '#363062',     # Navy
            'bg': '#ffffff',          # White background
            'text': '#2c3e50',        # Dark blue text
            'success': '#4F959D',     # Medium teal for success
            'error': '#e74c3c',       # Keep red for errors
            'light_bg': '#f5f7fa'     # Light background
        }
        
        # Header
        header = Frame(self.window, bg=colors['primary'], pady=10)
        header.pack(fill=tk.X)
        
        tk.Label(header, 
               text="Add New Product", 
               font=("Segoe UI", 14, "bold"),
               bg=colors['primary'],
               fg="white").pack(padx=20)
        
        # Main form container
        form_container = Frame(self.window, bg=colors['bg'], padx=25, pady=10)
        form_container.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable frame for forms with reduced padding
        canvas = tk.Canvas(form_container, bg=colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        
        scrollable_frame = Frame(canvas, bg=colors['bg'])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields with reduced spacing
        for i, (label, props) in enumerate(self.prod_specs.items()):
            field_frame = Frame(scrollable_frame, bg=colors['bg'], pady=3)  # Reduced padding
            field_frame.pack(fill=tk.X, pady=4)  # Reduced spacing between fields
            
            # Label with custom styling
            tk.Label(field_frame, 
                   text=label, 
                   font=("Segoe UI", 10, "bold"),
                   bg=colors['bg'],
                   fg=colors['text']).grid(row=0, column=0, sticky="w", pady=(0,2))  # Reduced padding
            
            # Entry with custom styling
            input_type = props['entry_type']
            if input_type == 'small_box':
                entry = tk.Entry(field_frame, 
                              font=("Segoe UI", 10),
                              width=50,
                              relief=tk.SOLID,
                              bd=1)
            elif input_type == 'large_box':
                entry = tk.Text(field_frame, 
                             font=("Segoe UI", 10),
                             width=50, 
                             height=3,  # Reduced height
                             relief=tk.SOLID,
                             bd=1)
            
            entry.grid(row=1, column=0, sticky="ew")
            
            # Required indicator
            if props.get('required', False):
                tk.Label(field_frame, 
                       text="*Required", 
                       font=("Segoe UI", 8),
                       bg=colors['bg'],
                       fg=colors['error']).grid(row=0, column=1, sticky="w", padx=5)
            
            # Error message label
            message_label = tk.Label(field_frame, 
                                  text="", 
                                  font=("Segoe UI", 8),
                                  bg=colors['bg'],
                                  fg=colors['error'])
            message_label.grid(row=2, column=0, sticky="w")
            
            self.message_labels[label] = message_label
            self.entries[label] = (entry, props['validation'], props.get('required', False))
        
        # Buttons container
        button_frame = Frame(self.window, bg=colors['light_bg'], pady=10)  # Reduced padding
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
        
        # Add item button
        submit_btn = tk.Button(button_frame, 
                             text="Add Item", 
                             command=self.add_item_submit,
                             font=("Segoe UI", 10, "bold"),
                             bg=colors['success'],
                             fg="white",
                             padx=15,
                             pady=5,
                             relief=tk.FLAT)
        submit_btn.pack(side=tk.RIGHT, padx=20)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Footer with watermark
        watermark = tk.Label(button_frame, 
                          text="Made by CodeByte",
                          font=("Segoe UI", 8, "italic"),
                          fg="#a0a0a0",
                          bg=colors['light_bg'])
        watermark.pack(side=tk.BOTTOM, pady=(10, 0))
        
    def add_item_submit(self):
        # Clear previous error messages
        for label in self.message_labels:
            self.message_labels[label].config(text="")
            
        # Fix validation issue by passing self.logic.validate_input directly
        validation_passed = True
        product_data = {}
        
        for label, (entry, validation_type, is_required) in self.entries.items():
            # Get the value depending on entry type
            if isinstance(entry, tk.Text):
                value = entry.get("1.0", "end-1c")
            else:
                value = entry.get()
                
            # Validate using the validation method from logic
            if not self.logic.validate_input(value, validation_type, is_required, label, self.message_labels):
                validation_passed = False
            else:
                product_data[label] = value
        
        if not validation_passed:
            return
        
        try:
            self.inventory_system.add_item_to_database(product_data)
            self.window.destroy()
            messagebox.showinfo("Success", "Item added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))