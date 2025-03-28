import requests
# Install requests from the VScode terminal with: "pip install requests"

# Import UI code
from ui.search_view_edit import SearchViewEdit
from ui.login_view import LoginView
from ui.display_default import DisplayDefault
from ui.add_item_view import AddItemView
from ui.remove_item_view import RemoveItemView
from ui.manage_fields_view import ManageFieldsView
# Import Database Code
from database.DatabaseSystem import *

class AI:
    def __init__(self, inventory_system):
        self.inventory_system = inventory_system
        self.api_key_gemini = "AIzaSyChLURtLM1Ldq_hl_6rj3IFB3AQpV-KoKE"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key_gemini}"
        # ----------------------------------------
        
    def make_Query(self, user_query):
        
        # Construct the API request payload
        payload = {
            "contents": [{
                "parts": [
                    {"text": "You are a database assistant. You will be provided the current database in JSON format. "
                             "The user may ask questions related to the inventory database, and you are responsible for answering "
                             "and, if needed, suggesting actions to update the inventory."},
                    {"text": str(user_query)},
                    {"text": f"Database snapshot:\n{self.get_database_json()}"}
                ]
            }]
        }

        headers = {"Content-Type": "application/json"}

        # Make the API request
        response = requests.post(self.api_url, headers=headers, json=payload)

        # Parse and return the response
        if response.status_code == 200:
            response_data = response.json()
            try:
                return response_data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                return "Error: Unexpected response format."
        else:
            return f"Error: API request failed with status code {response.status_code}"
            
    def get_database_json(self):
        try:
            database_items = self.inventory_system.get_all_items()
            database_json = database_items.to_json(orient="records", indent=4)
            return database_json
        except Exception as e:
            print("ERROR WITH DATABASE")
            return f"Error retrieving database: {str(e)}"
            