import pandas as pd
import sqlite3
import json

# To fetch Amount from Promotion Discount json data to
def extract_amount(discount_price):
    try:
        item_data = json.loads(discount_price)
        return float(item_data['Amount']) if 'Amount' in item_data else 0
    except (json.JSONDecodeError, TypeError):
        return 0

# Function to load the transformed data into SQLite
def load_data_to_sqlite(df):
    #SQLite database
    sqlite_db = "sales_database.db"
    
    try:
        # Business Rule 7: Load the transformed data into SQLite database
        conn = sqlite3.connect(sqlite_db)
        print("Connected to the database successfully.")

        conn.execute('''CREATE TABLE IF NOT EXISTS sales_data(
                    OrderId INT PRIMARY KEY,
                    OrderItemId INT,
                    QuantityOrdered INT,
                    ItemPrice INT,
                    PromotionDiscount FLOAT,
                    batch_id INT,
                    region CHARACTER(1),
                    total_sales INT,
                    net_sale FLOAT);''')
        print("Table 'sales_data' is ready or already exists.")

        # Insert the transformed data into the SQLite database
        df.to_sql('sales_data',con=conn,if_exists='replace', index=False)
        print("Data successfully inserted into the sales_data table.")
        conn.commit()
        print("Transaction committed successfully.")

        # SELECT query to fetch and display the data
        select_query = "SELECT COUNT(*) FROM sales_data;"  # Limit to 10 rows for viewing
        cursor = conn.cursor()
        cursor.execute(select_query)

        # Fetch the result (a tuple containing the count)
        row_count = cursor.fetchone()[0]

        # Print the count of rows
        print(f"Total number of rows in the 'sales_data' table: {row_count}")
    except sqlite3.DatabaseError as db_err:
        print(f"Database error occurred: {db_err}")
        # If there's an error, we roll back the transaction
        conn.rollback()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Rollback in case of any unexpected error
        conn.rollback()

    finally:
        # Ensure the connection is closed properly
        if conn:
            conn.close()
            print("Connection closed.")

# Function to count total records in the sales_data table
def count_total_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales_data;")
    total_records = cursor.fetchone()[0]
    print(f"Total number of records: {total_records}")

# Function to find total sales amount by region
def total_sales_by_region(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT region, SUM(total_sales) AS total_sales_by_region
        FROM sales_data
        GROUP BY region;
    """)
    sales_by_region = cursor.fetchall()
    print("Total Sales Amount by Region:")
    for row in sales_by_region:
        print(f"Region: {row[0]}, Total Sales: {row[1]}")

# Function to find average sales amount per transaction
def average_sales_per_transaction(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(total_sales) AS average_sales_per_transaction FROM sales_data;")
    avg_sales = cursor.fetchone()[0]
    print(f"Average Sales Amount per Transaction: {avg_sales}")

# Function to check for duplicate OrderId values
def check_duplicate_orderid(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT OrderId, COUNT(*) AS occurrences
        FROM sales_data
        GROUP BY OrderId
        HAVING COUNT(*) > 1;
    """)
    duplicates = cursor.fetchall()
    if duplicates:
        print("Duplicate OrderIds found:")
        for row in duplicates:
            print(f"OrderId: {row[0]}, Occurrences: {row[1]}")
    else:
        print("No duplicate OrderIds found.")

#Excel data
order_region_a = "order_region_a.xlsx"
order_region_b = "order_region_b.xlsx"

#Extract data
data_frame1 = pd.read_excel(order_region_a)
data_frame1['region'] = 'A'     #adding region A to dataframe
data_frame2 = pd.read_excel(order_region_b)
data_frame2['region'] = 'B'     #adding region B to dataframe

print("Count of Data from region a:"+"\n",data_frame1.shape)
print("Count of Data from region b:"+"\n",data_frame2.shape)

#Combine data
combined_data_frame = pd.concat([data_frame1,data_frame2])

print("The count of combined data:", combined_data_frame.shape)

# Transform the data
# Business Rule 4: Ensuring there are no duplicate entries based on 'OrderId'
combined_data_frame = combined_data_frame.drop_duplicates(subset=['OrderId'])
print("After removing duplicate the count of combined data:", combined_data_frame.shape)

# Business Rule 2: Adding a column 'total_sales' (QuantityOrdered * ItemPrice)
combined_data_frame['total_sales'] = combined_data_frame['QuantityOrdered'] * combined_data_frame['ItemPrice']

# print("Total sales:", combined_data_frame['total_sales'].head())

combined_data_frame['PromotionDiscount'] = combined_data_frame['PromotionDiscount'].apply(extract_amount)
# print("Promotion Discount: ", combined_data_frame['PromotionDiscount'].head())


# Business Rule 5: Adding a new column 'net_sale' (total_sales - PromotionDiscount)
combined_data_frame['net_sale'] = combined_data_frame['total_sales'] - combined_data_frame['PromotionDiscount']

# Business Rule 6: Excluding orders where net sale is negative or zero
combined_data_frame = combined_data_frame[combined_data_frame['net_sale']>0]

print("Combined data: \n", combined_data_frame.head())

# Load the data into SQLite database
load_data_to_sqlite(combined_data_frame)

try:
    # Connect to the SQLite database to run validation queries
    conn = sqlite3.connect('sales_database.db')
    
    # Validate data using SQL queries
    count_total_records(conn)
    total_sales_by_region(conn)
    average_sales_per_transaction(conn)
    check_duplicate_orderid(conn)

except sqlite3.Error as e:
    print(f"SQLite error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure the connection is closed, even if there was an error
    if conn:
        conn.close()
