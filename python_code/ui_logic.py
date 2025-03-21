import re

class UILogic:
    def __init__(self, inventory_system):
        self.inventory_system = inventory_system
        self.patterns = {
            'string': r'^[a-zA-Z0-9\s]+$',  # Allow a-z, A-Z, 0-9
            'int': r'^[+-]?\d+$',  # Allow + or -, and 0-9
            'float': r'^[+-]?\d+\.\d+$'  # Allow + or -, 0-9, and period "."
        }

    def get_inventory_data(self):
        self.inventory_system.cursor.execute(f"PRAGMA table_info({self.inventory_system.items_table})")
        columns = [column[1] for column in self.inventory_system.cursor.fetchall()]
        query = f"SELECT {', '.join(columns)} FROM {self.inventory_system.items_table}"
        self.inventory_system.cursor.execute(query)
        records = self.inventory_system.cursor.fetchall()
        return columns, records

    def get_add_item_specs(self, window):
        entries = {}
        message_labels = {}
        self.inventory_system.cursor.execute(f"SELECT field_name, entry_type, validation_type, required FROM {self.inventory_system.fields_table}")
        fields = self.inventory_system.cursor.fetchall()
        prod_specs = {}
        for field_name, entry_type, validation_type, required in fields:
            prod_specs[field_name] = {
                'type': 'text_box_s' if validation_type in ['string', 'int', 'float'] else 'text_box_l',
                'entry_type': entry_type,
                'validation': validation_type,
                'required': bool(required)
            }
        return entries, message_labels, prod_specs

    def validate_entries(self, entries, message_labels):
        validation_passed = True
        product_data = {}
        for label, (entry, validation_type, is_required) in entries.items():
            value = entry.get("1.0", "end-1c") if isinstance(entry, tk.Text) else entry.get()
            if not self.validate_input(value, validation_type, is_required, label, message_labels):
                validation_passed = False
            else:
                product_data[label] = value
        return validation_passed, product_data

    def get_add_field_specs(self, popup):
        field_name_entry = tk.Entry(popup)
        field_name_entry.pack()
        entry_type = tk.StringVar()
        entry_type.set("")
        small_box_button = tk.Button(popup, text="Small Box", command=lambda: entry_type.set("small_box"))
        small_box_button.pack(pady=5)
        large_box_button = tk.Button(popup, text="Large Box", command=lambda: entry_type.set("large_box"))
        large_box_button.pack(pady=5)
        validation_type = tk.StringVar()
        validation_type.set("")
        string_box_button = tk.Button(popup, text="String", command=lambda: validation_type.set("string"))
        string_box_button.pack(pady=5)
        int_box_button = tk.Button(popup, text="Integer", command=lambda: validation_type.set("int"))
        int_box_button.pack(pady=5)
        float_box_button = tk.Button(popup, text="Decimal Value", command=lambda: validation_type.set("float"))
        float_box_button.pack(pady=5)
        required = tk.StringVar()
        required.set("")
        required_button = tk.Button(popup, text="Required", command=lambda: required.set("1"))
        required_button.pack(pady=5)
        not_required_button = tk.Button(popup, text="Not Required", command=lambda: required.set("0"))
        not_required_button.pack(pady=5)
        return field_name_entry, entry_type, validation_type, required

    def get_existing_fields(self):
        self.inventory_system.cursor.execute(f"SELECT field_name FROM {self.inventory_system.fields_table}")
        fields = [row[0] for row in self.inventory_system.cursor.fetchall()]
        return fields

    def validate_field_specs(self, field_name, entry_type_value, validation_type_value, required_value):
        if " " in field_name:
            messagebox.showerror("Error", "Name cannot contain spaces.")
            return False
        if entry_type_value not in ["small_box", "large_box"]:
            messagebox.showerror("Error", "Entry type must be 'small_box', or 'large_box'.")
            return False
        if validation_type_value not in ["string", "int", "float"]:
            messagebox.showerror("Error", "Validation type must be 'string', 'int', or 'float'.")
            return False
        if required_value not in ["0", "1"]:
            messagebox.showerror("Error", "Required must be 0 or 1.")
            return False
        return True

    def validate_input(self, value, validation_type, is_required, label, message_labels):
        if is_required and not value.strip():
            message_labels[label].config(text=f"{label} is required.")
            return False
        if not is_required and not value.strip():
            return True
        if validation_type == 'string' and not re.match(self.patterns['string'], value):
            message_labels[label].config(text=f"{label} contains invalid characters.")
            return False
        if validation_type == 'int' and not re.match(self.patterns['int'], value):
            message_labels[label].config(text=f"{label} must be an integer.")
            return False
        if validation_type == 'float' and not re.match(self.patterns['float'], value):
            message_labels[label].config(text=f"{label} must be a float (contain decimal point) ex. 0.00.")
            return False
        return True