import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Frame
from datetime import datetime
from DatabaseSystem import *
from ui import *

db = pd.DataFrame()

def main():
    # Create instance of the inventory System
    database = DatabaseSystem("Electronics Database", "inventory.db")
    
    # Display Menu for database instance
    database.start_ui()


if __name__ == "__main__":
    main()
