import unittest
from unittest.mock import MagicMock
from datetime import datetime
import sys
from pathlib import Path

# Add the parent directory to the sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ui.ui import UI

class TestActivityLog(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.ui = UI(self.mock_db)

    def test_log_entry_created_on_add_item(self):
        # Simulate adding an item
        self.ui.display_add_item()
        
        # Check if a log entry was created
        self.mock_db.add_log_entry.assert_called_with("Item added", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def test_log_entry_created_on_remove_item(self):
        # Simulate removing an item
        self.ui.display_remove_item()
        
        # Check if a log entry was created
        self.mock_db.add_log_entry.assert_called_with("Item removed", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    unittest.main()