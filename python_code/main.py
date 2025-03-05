import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Frame
from datetime import datetime

db = pd.DataFrame()

class InventorySystem:
    def __init__(self):
        self.inventory = []

    def add_product(self):
        product_id = simpledialog.askstring("Input", "Enter product ID:")
        if product_id is None:
            return
        category = simpledialog.askstring("Input", "Enter category:")
        if category is None:
            return
        name = simpledialog.askstring("Input", "Enter product name:")
        if name is None:
            return
        brand = simpledialog.askstring("Input", "Enter brand:")
        if brand is None:
            return
        try:
            price = float(simpledialog.askstring("Input", "Enter price: $"))
            if price is None:
                return
            quantity = int(simpledialog.askstring("Input", "Enter quantity:"))
            if quantity is None:
                return
        except ValueError:
            messagebox.showerror("Error", "Price and quantity must be numbers")
            return
        specifications = simpledialog.askstring("Input", "Enter specifications:")
        if specifications is None:
            return

        # Get time directly before adding product
        curr_time = datetime.now()
        
        new_product = {
            'product_id': product_id,
            'category': category,
            'name': name,
            'brand': brand,
            'price': price,
            'quantity': quantity,
            'specifications': specifications,
            'date': curr_time
        }
        self.inventory.append(new_product)
        messagebox.showinfo("Success", f"Product '{name}' added successfully")

    def remove_product(self):
        if not self.inventory:
            messagebox.showinfo("Info", "Inventory is empty")
            return

        product_id = simpledialog.askstring("Input", "Enter product ID to remove:")
        if product_id is None:
            return
        for product in self.inventory:
            if product['product_id'] == product_id:
                if product['quantity'] > 1:
                    product['quantity'] -= 1
                    messagebox.showinfo("Success", f"Decreased quantity of product '{product['name']}' by 1")
                else:
                    self.inventory.remove(product)
                    messagebox.showinfo("Success", "Product removed successfully")
                return
        messagebox.showerror("Error", "Product not found")

    def display_inventory(self):
        if not self.inventory:
            messagebox.showinfo("Info", "Inventory is empty")
            return

        inventory_list = "\n".join([f"ID: {product['product_id']}, Name: {product['name']}, Quantity: {product['quantity']}, Created: {product['date']}" for product in self.inventory])
        messagebox.showinfo("Current Inventory", inventory_list)

def main():
    system = InventorySystem()

    root = tk.Tk()
    root.title("Computer Parts Inventory System")
    root.geometry("700x500")
    root.configure(bg="#f0f0f0")  # Set background color
    
    # Create title frame
    title_frame = Frame(root, bg="#3498db", pady=15)
    title_frame.pack(fill=tk.X)
    
    title_label = tk.Label(title_frame, text="Computer Parts Inventory System", 
                          font=("Consolas", 16, "bold"), bg="#3498db", fg="white")
    title_label.pack()
    
    # Create main content frame
    content_frame = Frame(root, bg="#f0f0f0", pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create buttons with better styling
    button_style = {"font": ("Consolas", 11),
                   "bg": "#2980b9",
                   "fg": "white",
                   "width": 20,
                   "height": 2,
                   "borderwidth": 0,
                   "cursor": "hand2"}
    
    tk.Button(content_frame, text="Display Inventory", command=system.display_inventory, 
             **button_style).pack(pady=10)
    
    tk.Button(content_frame, text="Add Product", command=system.add_product,
             **button_style).pack(pady=10)
    
    tk.Button(content_frame, text="Remove Product", command=system.remove_product,
             **button_style).pack(pady=10)
    
    tk.Button(content_frame, text="Exit", command=root.quit,
             bg="#e74c3c", fg="white", font=("Consolas", 11),
             width=20, height=2, borderwidth=0).pack(pady=20)
    
    # Add status bar
    status_bar = tk.Label(root, text="Inventory Online", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
