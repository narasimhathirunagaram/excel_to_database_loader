# Python script for Sales Data Processing

This Python script processes sales data from two different regions (Region A and Region B) and performs various transformations according to specified business rules. It loads the cleaned and transformed data into an SQLite database for further analysis and validation.

## Features

- **Extracts Data**: Reads sales data from Excel files for Region A and Region B.
- **Transforms Data**: Applies business rules such as adding calculated columns, excluding negative sales, and removing duplicates.
- **Loads Data**: Inserts the transformed data into an SQLite database.
- **Validates Data**: Runs validation queries to check for the total number of records, total sales by region, average sales per transaction, and duplicate `OrderId` values.
- **Error Handling**: Implements exception handling for database and unexpected errors.

## Files

- **sales_database.db**: SQLite database containing the processed sales data.
- **order_region_a.xlsx**: Excel file containing sales data for Region A.
- **order_region_b.xlsx**: Excel file containing sales data for Region B.
- **sales_data_processing.py**: Python script that processes the data and loads it into the SQLite database.

## Business Rules

1. Combine data from Region A and Region B into a single table.
2. Add a column `total_sales` calculated as `QuantityOrdered * ItemPrice`.
3. Add a column `region` to identify the region of the sales record (A or B).
4. Remove duplicate records based on `OrderId`.
5. Add a column `net_sale` calculated as `total_sales - PromotionDiscount`.
6. Exclude orders where `net_sale` is less than or equal to zero.

## Setup and Run Instructions

### Step 1: Cloning the Repository :
To clone this repository, open your terminal and run the following command:
git clone <repository_url>

### Step 2: Set Up a Virtual Environment
To create a virtual environment for the project, run the following command:
python3 -m venv venv

### Step 3: Activate the Virtual Environment
source venv/bin/activate

### Step 4: Install the required libraries
pip install pandas openpyxl

### Step 5: Create requirements.txt
pip freeze > requirements.txt

## Usage

### Step 1: Prepare the excel files
Ensure the necessary Excel files (order_region_a.xlsx and order_region_b.xlsx) are available in the working directory.

### Step 2: Run the python script
python3 excel_to_database_loader.py

