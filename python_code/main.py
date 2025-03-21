import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Frame
from datetime import datetime
from DatabaseSystem import *
from ui import *

db = pd.DataFrame()

# main.py
from DatabaseSystem import DatabaseSystem
from ui import UI

def main():
    # Create instance of the inventory System
    database = DatabaseSystem("Electronics Database", "inventory.db")
    
    # Create UI instance and set it in the database system
    ui = UI(database)
    database.set_ui(ui)
    
    # Display Menu for database instance
    ui.display_menu()

if __name__ == "__main__":
    main()
