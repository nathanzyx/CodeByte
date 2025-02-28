import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog
db = pd.DataFrame()

class InventorySystem:
    def __init__(self):
        self.inventory = []

    def add_product(self):
        product_id = simpledialog.askstring("Input", "Enter product ID:")
        category = simpledialog.askstring("Input", "Enter category:")
        name = simpledialog.askstring("Input", "Enter product name:")
        brand = simpledialog.askstring("Input", "Enter brand:")
        try:
            price = float(simpledialog.askstring("Input", "Enter price: $"))
            quantity = int(simpledialog.askstring("Input", "Enter quantity:"))
        except ValueError:
            messagebox.showerror("Error", "Price and quantity must be numbers")
            return
        specifications = simpledialog.askstring("Input", "Enter specifications:")

        new_product = {
            'product_id': product_id,
            'category': category,
            'name': name,
            'brand': brand,
            'price': price,
            'quantity': quantity,
            'specifications': specifications
        }
        self.inventory.append(new_product)
        messagebox.showinfo("Success", f"Product '{name}' added successfully")

    def remove_product(self):
        if not self.inventory:
            messagebox.showinfo("Info", "Inventory is empty")
            return

        product_id = simpledialog.askstring("Input", "Enter product ID to remove:")
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

        inventory_list = "\n".join([f"ID: {product['product_id']}, Name: {product['name']}, Quantity: {product['quantity']}" for product in self.inventory])
        messagebox.showinfo("Current Inventory", inventory_list)

def main():
    system = InventorySystem()

    root = tk.Tk()
    root.title("Computer Parts Inventory System")
    root.geometry("400x300")

    tk.Button(root, text="Display Inventory", command=system.display_inventory).pack(pady=10)
    tk.Button(root, text="Add Product", command=system.add_product).pack(pady=10)
    tk.Button(root, text="Remove Product", command=system.remove_product).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
