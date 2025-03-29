import customtkinter as ctk
from tkinter import messagebox

class AddItemView:
    def __init__(self, parent, logic, inventory_system):
        self.window = ctk.CTkToplevel(parent)
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
        header = ctk.CTkFrame(self.window, fg_color=colors['primary'], corner_radius=0)
        header.pack(fill=ctk.X)
        
        ctk.CTkLabel(header, 
               text="Add New Product", 
               font=("Segoe UI", 14, "bold"),
               text_color="white").pack(padx=20)
        
        # Main form container
        form_container = ctk.CTkFrame(self.window, fg_color=colors['bg'], corner_radius=0)
        form_container.pack(fill=ctk.BOTH, expand=True, padx=25, pady=10)
        
        # Create scrollable frame for forms
        canvas = ctk.CTkCanvas(form_container, bg=colors['bg'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(form_container, orientation="vertical", command=canvas.yview)
        
        scrollable_frame = ctk.CTkFrame(canvas, fg_color=colors['bg'])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        for i, (label, props) in enumerate(self.prod_specs.items()):
            field_frame = ctk.CTkFrame(scrollable_frame, fg_color=colors['bg'])
            field_frame.pack(fill=ctk.X, pady=4)
            
            # Label
            ctk.CTkLabel(field_frame, 
                   text=label, 
                   font=("Segoe UI", 10, "bold"),
                   text_color=colors['text']).grid(row=0, column=0, sticky="w", pady=(0, 2))
            
            # Entry
            input_type = props['entry_type']
            if input_type == 'small_box':
                entry = ctk.CTkEntry(field_frame, 
                              font=("Segoe UI", 10),
                              width=400)
            elif input_type == 'large_box':
                entry = ctk.CTkTextbox(field_frame, 
                             font=("Segoe UI", 10),
                             width=400, 
                             height=80)
            
            entry.grid(row=1, column=0, sticky="ew")
            
            # Required indicator
            if props.get('required', False):
                ctk.CTkLabel(field_frame, 
                       text="*Required", 
                       font=("Segoe UI", 8),
                       text_color=colors['error']).grid(row=0, column=1, sticky="w", padx=5)
            
            # Error message label
            message_label = ctk.CTkLabel(field_frame, 
                                  text="", 
                                  font=("Segoe UI", 8),
                                  text_color=colors['error'])
            message_label.grid(row=2, column=0, sticky="w")
            
            self.message_labels[label] = message_label
            self.entries[label] = (entry, props['validation'], props.get('required', False))
        
        # Buttons container
        button_frame = ctk.CTkFrame(self.window, fg_color=colors['light_bg'], corner_radius=0)
        button_frame.pack(fill=ctk.X, side=ctk.BOTTOM, pady=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(button_frame, 
                             text="Cancel", 
                             command=self.window.destroy,
                             font=("Segoe UI", 10),
                             fg_color="white",
                             text_color=colors['text'])
        cancel_btn.pack(side=ctk.LEFT, padx=20)
        
        # Add item button
        submit_btn = ctk.CTkButton(button_frame, 
                             text="Add Item", 
                             command=self.add_item_submit,
                             font=("Segoe UI", 10, "bold"),
                             fg_color=colors['success'],
                             text_color="white")
        submit_btn.pack(side=ctk.RIGHT, padx=20)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Footer with watermark
        watermark = ctk.CTkLabel(button_frame, 
                          text="Made by CodeByte",
                          font=("Segoe UI", 8, "italic"),
                          text_color="#a0a0a0")
        watermark.pack(side=ctk.BOTTOM, pady=(10, 0))
        
    def add_item_submit(self):
        # Clear previous error messages
        for label in self.message_labels:
            self.message_labels[label].config(text="")
            
        # Fix validation issue by passing self.logic.validate_input directly
        validation_passed = True
        product_data = {}
        
        for label, (entry, validation_type, is_required) in self.entries.items():
            # Get the value depending on entry type
            if isinstance(entry, ctk.CTkTextbox):
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