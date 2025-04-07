import unittest
from unittest.mock import MagicMock, patch
from database.DatabaseSystem import DatabaseSystem
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from ui.login_view import LoginView

class TestAddToFieldsTable(unittest.TestCase):
    def setUp(self):
        # Mock the database connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.patcher = patch('sqlite3.connect', return_value=self.mock_conn)
        self.patcher.start()
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Create an instance of the DatabaseSystem
        self.db_system = DatabaseSystem("TestDB", "test.db")
        self.db_system.conn = self.mock_conn
        self.db_system.cursor = self.mock_cursor
        
        

    def tearDown(self):
        # Stop the patcher
        self.patcher.stop()


    # 
    #   Test: UT-01-CB
    #   Testing: add_to_fields_table
    #
    def test_add_to_fields_table(self):
        # Mock fetchone
        self.mock_cursor.fetchone.return_value = (0,)

        # Call method under test
        result = self.db_system.add_to_fields_table("new_field", "small_box", "string", True)

        # Check if the result is True
        self.assertTrue(result)
        
        
    # 
    #   Test: UT-02-CB
    #   Testing: add_to_fields_table
    #
    @patch.object(DatabaseSystem, 'log_message')
    def test_remove_to_fields_table(self, mock_log_message):
        field_to_remove = "field_to_delete"
        self.mock_cursor.reset_mock()
        self.mock_conn.reset_mock()


        self.db_system.remove_to_fields_table(field_to_remove)

        # Check if execute was called once with the correct SQL
        self.mock_cursor.execute.assert_called_once_with(
            f"DELETE FROM {self.db_system.fields_table} WHERE field_name = ?",(field_to_remove,))

        #Check if commit was called once
        self.mock_conn.commit.assert_called_once()

        mock_log_message.assert_called_once_with(f"Field Removed: field_name:{field_to_remove}")
    
    #
    #   Test: UT-03-CB
    #   Testing: add_item_to_database
    #        
    def test_add_item_to_database(self):

        product_data = {
            "id": "1",
            "name": "name",
            "quantity": 1,
            "price": 1.0,
            "category": "category",
            "brand": "brand",
            "description": "description",
        }

        result = self.db_system.add_item_to_database(product_data)

        self.assertTrue(result)
        
    #
    # Test: UT-04-TB
    #
    @patch.object(DatabaseSystem, 'log_message') # Mock log_message for this test
    def test_remove_item_from_database(self, mock_log_message):
    
        item_id_to_remove = "1"
        count_to_remove = 1
        initial_quantity = 10
        expected_new_quantity = initial_quantity - count_to_remove

        # Mock fetchone 
        self.mock_cursor.fetchone.return_value = (initial_quantity,)

        # Reset mock 
        self.mock_cursor.reset_mock() 
        self.mock_conn.reset_mock()

        #  Call method under test
        try:
            self.db_system.remove_item_from_database(item_id_to_remove, count_to_remove)
            # Test implicitly passes the "no error" check if it reaches here
        except ValueError as e:
            self.fail(f"remove_item_from_database raised ValueError unexpectedly: {e}")

        select_sql = f"SELECT quantity FROM {self.db_system.items_table} WHERE id=?"
        self.mock_cursor.execute.assert_any_call(select_sql, (item_id_to_remove,))
        update_sql = f"UPDATE {self.db_system.items_table} SET quantity=? WHERE id=?"
        self.mock_cursor.execute.assert_any_call(update_sql, (expected_new_quantity, item_id_to_remove))

        self.mock_conn.commit.assert_called_once()

        mock_log_message.assert_called_once_with(f"Item Removed: id:{item_id_to_remove}, count:{count_to_remove}")
            
    #
    # Test: UT-05-TB
    #
    def test_search_items(self):
        fields = []  # No fields selected
        query = "anything"  # Query doesn't matter here since no fields are selected
        
        self.mock_cursor.fetchall.return_value = []

        result_df = self.db_system.search_items(fields, query)

        self.assertTrue(result_df.empty)  # Ensure DataFrame is empty
        
    #
    # Test: UT-06-TB
    #
    @patch.object(DatabaseSystem, 'log_message')
    def test_update_item(self, mock_log_message):
        item_id = 1
        new_data = {
            'name': 'Updated Item',
            'price': 20.99,
            'id': 2
        }
        
        # Mock database calls
        self.mock_cursor.execute.reset_mock()
        self.mock_conn.reset_mock()

        # Act: Call the method under test
        result = self.db_system.update_item(item_id, new_data)
        
        self.assertTrue(result)

    #
    # Test: UT-07-TB
    #
    @patch.object(DatabaseSystem, 'log_message')
    @patch('PyQt6.QtWidgets.QInputDialog.getText')
    @patch('PyQt6.QtWidgets.QMessageBox.question')
    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_clear_database(self, mock_info, mock_question, mock_get_text, mock_log_message):
        # Mock QInputDialog to simulate user providing the correct password
        mock_get_text.return_value = ("correct_password", True)  # password, ok
        
        mock_question.return_value = QMessageBox.StandardButton.Yes
        
        # Mock database cursor and connection
        self.mock_cursor.execute.reset_mock()
        self.mock_conn.reset_mock()
        
        self.db_system.password = "correct_password"
        self.db_system.account_exists = MagicMock(return_value=True)
        
        result = self.db_system.clear_database()

        # Check if method returns true on successfull execution
        self.assertTrue(result)
        
        
if __name__ == "__main__":
    unittest.main()