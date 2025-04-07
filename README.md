# Electronics Inventory Management System

## Overview
The **Electronics Inventory Management System** is a software application designed to help store operators efficiently manage electronic product inventory. It allows users to **add, update, remove, and search for products** in a centralized database.

We focused on establishing the core product data model and implementing fundamental CRUD (Create, Read, Update, Delete) functionality for inventory items, specifically the ability to add and remove products from the database. At its core the program performs the following.


-  **Product Database**: Add, update, and delete inventory items.

-  **Search & Filter**: Find products easily using search and filters, enhanced by AI.

-  **Admin Authentication**: Lock inventory modification behind a login system.

-  **Activity Logging**: Keep track of actions performed across the database.

## Noteable Features

- **Custom Fields**: Add custom fields to enhance efficiency of searching and user workflow.

- **Image/File Support**: Support for file types *png*, *jpg*, *jpeg*, *bmp*, and *gif*. Include any number of supported files with inventory items.

- **AI Assistant**: An assistant embedded in the programs dashboard powered by *Google Gemini 1.5 Flash* to assist with questions involving inventory.

- **Relevancy System**: If a traditional search yields no results, our relevancy system powered by *Google Gemini 1.5 Flash* will recommend inventory items relevant to what the user had searched.

## Setup

### Method 1 (Windows & Linux)

1. **Install `main.exe` from [Google Drive](https://drive.google.com/file/d/16scsfChKEYHgWdO19UaBUD2ns5oAubhD/view?usp=drive_link).**

2. **Run `main.exe` file.**
 - For Linux, `.exe` files are not supported however can be run using *Wine* or another comparable program.
 - It is recommended to keep `main.exe` in a seperate folder for orgranization, as the *database* and *activity log* file will be created in the same directory.

### Method 2

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nathanzyx/CodeByte.git
    ```

2. **Navigate into the project directory:**
    ```bash
    cd Codebyte
    ```

3. **Run `make setup` to install the required dependicies:**
    ```bash
    make setup
    ```

4. **Run `make run` to start the application:**
    ```bash
    make run
    ```

5. **Run `make clean` to remove unnecessary files:**
    ```bash
    make clean
    ```

### Usage

-   **Adding a Product:**
    -   Navigate to the "Add Product" page.
    -   Fill in the product details and submit.
-   **Deleting Products:**
    - Navigate to the "Remove Product" page.
    - Enter the product ID and the quantity to be removed.
    - Submit to remove the specified product quantity.

### Implemented User Stories (Iteration 1)

* P0: Remove Products from Database
* P0: Add Products to Database
* P0: Product Focused Database

### Next Steps (Goals for Iteration 2)

-   Implement product updating functionality.
-   Implement advanced search and filtering options.
-   Implement user authentication and basic admin login.
### Iteration 3  
-   Relevancy System
-   Activity Log
-   AI Feature




