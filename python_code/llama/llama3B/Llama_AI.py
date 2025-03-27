import sys
import os
import json

#
#   PLEASE READ
#       Follow the instructions in this video: https://www.youtube.com/watch?v=fYThzJCZJds&ab_channel=AleksandarHaberPhD
#           Place the env1 folder (the virtual environment in the llama3B folder)
#           Place all of the llama models files and folders into a folder in llama3B folder called 'model'
#           Adjust the modelPath to variable to point to the 'model' folder


# Import UI code
from ui.search_view_edit import SearchViewEdit
from ui.login_view import LoginView
from ui.display_default import DisplayDefault
from ui.add_item_view import AddItemView
from ui.remove_item_view import RemoveItemView
from ui.manage_fields_view import ManageFieldsView
# Import Database Code
from database.DatabaseSystem import *
# import llama.llama3B as AI_Path

# For Running Llama ----
from transformers import pipeline
import torch
    # Path to where the AI is kept (Replace with yours since i cant download the AI model to github (its 16GB))
modelPath = "C:\\Users\\natht\\CodeByte\\python_code\\llama\\Llama3B\\model"
# ---------------------

class Llama_AI:
    def __init__(self, inventory_system):
        self.inventory_system = inventory_system
        
        # Define AI related variables ------------
            # Define the AI model
        self.pipe = pipeline(
            "text-generation",
            model = modelPath,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.function_descriptions = {
            "get_database_json": "returns entire database as JSON"
        }
        # ----------------------------------------
        
    def make_Query(self, user_query):
        # Create the User's Message
        message = [
            {"role": "system", "content": "You are a database assistant, you will be provided the database in JSON format and the user may ask questions relating to the database inventory, it is your responsibility to answer."},
            {"role": "user", "content": str(user_query)},
            {"role": "database", "content": self.get_database_json()}
        ]
        # Response object
        response = self.pipe(
            message,
            max_new_tokens=500,
        )
        # Get Repsonse
        outputResponse = response[0]["generated_text"][-1]
        # Store AI response in file (prbably un-needed)
        with open('output.txt', 'w', encoding="utf-8") as text_file:
            text_file.write(outputResponse['content'])
            
        return outputResponse['content']
            
    def get_database_json(self):
        try:
            database_items = self.inventory_system.get_all_items()
            database_json = database_items.to_json(orient="records", indent=4)
            # print("Database Output: " + str(database_json))
            return database_json
        except Exception as e:
            print("ERROR RETURNING DATABASE")
            return f"Error retrieving database: {str(e)}"
            