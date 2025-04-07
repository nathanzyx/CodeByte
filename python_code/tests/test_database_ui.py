# Unit tests for DatabaseSystem and UI classes.
import unittest
import sys
from pathlib import Path

# Ensure parent directory is in the path so imports work
sys.path.append(str(Path(__file__).resolve().parent.parent))

from unittest.mock import MagicMock, patch
from python_code.database.DatabaseSystem import DatabaseSystem
from python_code.ui import UI

class TestDatabaseSystem(unittest.TestCase):
    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.patcher = patch('sqlite3.connect', return_value=self.mock_conn)
        self.patcher.start()
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.db_system = DatabaseSystem("TestDB", "test.db")

    def tearDown(self):
        self.patcher.stop()

    def test_table_exists(self):
        self.mock_cursor.fetchone.return_value = True
        self.assertTrue(self.db_system.table_exists("products"))
        self.mock_cursor.fetchone.return_value = None
        self.assertFalse(self.db_system.table_exists("products"))

    def test_create_fields_table(self):
        self.db_system.create_fields_table()
        self.mock_cursor.execute.assert_called()
        self.mock_conn.commit.assert_called()

    def test_create_products_table(self):
        self.mock_cursor.fetchall.return_value = [("id", "string"), ("name", "string")]
        self.db_system.create_products_table()
        self.mock_cursor.execute.assert_called()
        self.mock_conn.commit.assert_called()

    def test_add_to_fields_table(self):
        self.mock_cursor.fetchall.return_value = []  # Simulate no existing fields
        result = self.db_system.add_to_fields_table("new_field", "small_box", "string", True)
        self.assertTrue(result)

    def test_remove_from_fields_table(self):
        self.db_system.remove_to_fields_table("test_field")
        self.mock_cursor.execute.assert_called_with(
            "DELETE FROM fields WHERE field_name = ?", ("test_field",)
        )

    def test_add_item_to_database(self):
        self.mock_cursor.fetchall.return_value = [("id",), ("name",), ("quantity",)]
        product_data = {"id": "123", "name": "Laptop", "quantity": "10"}
        result = self.db_system.add_item_to_database(product_data)
        self.assertTrue(result)

    def test_remove_item_from_database(self):
        self.mock_cursor.fetchone.return_value = (10,)  # Simulate current quantity
        self.db_system.remove_item_from_database("123", 5)
        self.mock_cursor.execute.assert_called()

    @patch('tkinter.messagebox.askyesno')
    def test_clear_database(self, mock_askyesno):
        mock_askyesno.return_value = True
        self.db_system.clear_database()
        self.mock_cursor.execute.assert_called()
        self.mock_conn.commit.assert_called()


class TestUI(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.ui = UI(self.mock_db)

    @patch('tkinter.Toplevel')
    @patch('tkinter.ttk.Treeview')
    def test_display_inventory(self, mock_treeview, mock_toplevel):
        self.mock_db.cursor.fetchall.return_value = [(1, "Laptop", 10)]
        self.ui.display_inventory(["id", "name", "quantity"])
        mock_treeview.return_value.insert.assert_called()

    @patch('tkinter.Toplevel')
    @patch('tkinter.Entry')
    def test_display_add_item(self, mock_entry, mock_toplevel):
        prod_specs = {
            'name': {
                'type': 'text_box_s', 'entry_type': 'small_box',
                'validation': 'string', 'required': True
            }
        }
        self.ui.display_add_item(prod_specs)
        mock_toplevel.assert_called_once()

    @patch('tkinter.Toplevel')
    @patch('tkinter.Entry')
    def test_display_remove_item(self, mock_entry, mock_toplevel):
        self.ui.display_remove_item()
        mock_toplevel.assert_called_once()

    @patch('tkinter.Tk')
    def test_display_menu(self, mock_tk):
        self.ui.display_menu()
        mock_tk.assert_called_once()

    @patch('tkinter.Toplevel')
    def test_display_options(self, mock_toplevel):
        self.ui.display_options()
        mock_toplevel.assert_called_once()


if __name__ == '__main__':
    unittest.main()
