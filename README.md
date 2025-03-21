# Electronics Inventory Management System

### Overview
The **Electronics Inventory Management System** is a software application designed to help store operators efficiently manage electronic product inventory. It allows users to **add, update, remove, and search for products** in a centralized database.

This MVP represents the work completed during Iteration 1. We focused on establishing the core product data model and implementing fundamental CRUD (Create, Read, Update, Delete) functionality for inventory items, specifically the ability to add and remove products from the database.

### Features

-  **Product Database**: Add, update, and delete inventory items.

-  **Search & Filter**: Find products easily using search and filters.

-  **Admin Authentication**: Restrict certain actions to authorized personnel.

-  **Activity Logging**: Keep track of product modifications.

### Setup

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

### Testing

Running `make test` in the terminal will execute the necessary tests to verify the program's functionality and usability.

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
