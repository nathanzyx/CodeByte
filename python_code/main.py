import pandas as pd
from datetime import datetime
from database.DatabaseSystem import *
from ui.ui import *

db = pd.DataFrame()

# main.py
from database.DatabaseSystem import DatabaseSystem
from ui.ui import UI

def main():
    # Create instance of the inventory System
    database = DatabaseSystem("Electronics Database", "inventory.db")
    
    # Create UI instance and set it in the database system
    ui = UI(database)
    database.set_ui(ui)
    
    # Display Menu for database instance
    ui.display_menu()
    ui.run()

if __name__ == "__main__":
    main()
