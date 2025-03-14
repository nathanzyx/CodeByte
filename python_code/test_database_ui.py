import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch
from DatabaseSystem import DatabaseSystem
from ui import UI

class TestDatabaseSystem:
    @pytest.fixture
    def setup(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        with patch('sqlite3.connect', return_value=mock_conn) as patcher:
            mock_conn.cursor.return_value = mock_cursor
            db_system = DatabaseSystem("TestDB", "test.db")
            yield db_system, mock_conn, mock_cursor, patcher

    def test_table_exists(self, setup):
        db_system, mock_conn, mock_cursor, _ = setup
        mock_cursor.fetchone.return_value = True
        assert db_system.table_exists("products") is True
        
        mock_cursor.fetchone.return_value = None
        assert db_system.table_exists("products") is False

    def test_create_fields_table(self, setup):
        db_system, mock_conn, mock_cursor, _ = setup
        db_system.create_fields_table()
        assert mock_cursor.execute.called
        assert mock_conn.commit.called

    def test_create_products_table(self, setup):
        db_system, mock_conn, mock_cursor, _ = setup
        mock_cursor.fetchall.return_value = [("id", "string"), ("name", "string")]
        db_system.create_products_table()
        assert mock_cursor.execute.called
        assert mock_conn.commit.called

    def test_add_to_fields_table(self, setup):
        db_system, mock_conn, mock_cursor, _ = setup
        mock_cursor.fetchall.return_value = []  # No existing columns
        result = db_system.add_to_fields_table("new_field", "small_box", "string", True)
        assert result is True

    def test_remove_from_fields_table(self, setup):
        db_system, mock_conn, mock_cursor, _ = setup
        db_system.remove_to_fields_table("test_field")
        mock_cursor.execute.assert_called_with("DELETE FROM fields WHERE field_name = ?", 
            ("test_field",)
        )

    def test_add_item_to_database(self, setup):
        db_system, mock_conn, mock_cursor, _ = setup
        mock_cursor.fetchall.return_value = [("id",), ("name",), ("quantity",)]
        product_data = {"id": "123", "name": "Laptop", "quantity": "10"}
        result = db_system.add_item_to_database(product_data)
        assert result is True

    def test_remove_item_from_database(self, setup):
        db_system, mock_conn, mock_cursor, _ = setup
        mock_cursor.fetchone.return_value = (10,)  # Current quantity
        db_system.remove_item_from_database("123", 5)
        assert mock_cursor.execute.called

    @patch('tkinter.messagebox.askyesno')
    def test_clear_database(self, mock_askyesno, setup):
        db_system, mock_conn, mock_cursor, _ = setup
        mock_askyesno.return_value = True
        db_system.clear_database()
        assert mock_cursor.execute.called
        assert mock_conn.commit.called

class TestUI:
    @pytest.fixture
    def setup(self):
        mock_db = MagicMock()
        ui = UI(mock_db)
        return ui, mock_db

    @pytest.mark.parametrize("columns,expected_data", [
        (["id", "name", "quantity"], [(1, "Laptop", 10)]),
    ])
    def test_display_inventory(self, setup, columns, expected_data):
        ui, mock_db = setup
        with patch('tkinter.Toplevel'), patch('tkinter.ttk.Treeview') as mock_treeview:
            mock_db.cursor.fetchall.return_value = expected_data
            ui.display_inventory(columns)
            assert mock_treeview.return_value.insert.called

    @patch('tkinter.Toplevel')
    @patch('tkinter.Entry')
    def test_display_add_item(self, mock_entry, mock_toplevel, setup):
        ui, mock_db = setup
        prod_specs = {
            'name': {'type': 'text_box_s', 'entry_type': 'small_box', 
                    'validation': 'string', 'required': True}
        }
        ui.display_add_item(prod_specs)
        mock_toplevel.assert_called_once()

    @patch('tkinter.Toplevel')
    @patch('tkinter.Entry')
    def test_display_remove_item(self, mock_entry, mock_toplevel, setup):
        ui, mock_db = setup
        ui.display_remove_item()
        mock_toplevel.assert_called_once()

    @patch('tkinter.Tk')
    def test_display_menu(self, mock_tk, setup):
        ui, mock_db = setup
        ui.display_menu()
        mock_tk.assert_called_once()

    @patch('tkinter.Toplevel')
    def test_display_options(self, mock_toplevel, setup):
        ui, mock_db = setup
        ui.display_options()
        mock_toplevel.assert_called_once()

if __name__ == '__main__':
    pytest.main()
