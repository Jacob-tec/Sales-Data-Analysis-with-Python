import pandas as pd
import matplotlib.pyplot as plt
import io

# --- 1. Create a dummy sales dataset ---
# In a real scenario, you would load this from a CSV file:
# df = pd.read_csv('sales_data.csv')

# For demonstration, we'll create a string with CSV data.
# This data includes some common issues like missing values,
# incorrect data types (e.g., 'Price' as string), and potential duplicates.
csv_data = """Date,Product,Quantity,Price,Region
2023-01-01,Laptop,2,1200.00,North
2023-01-01,Mouse,5,25.50,North
2023-01-02,Keyboard,3,75.00,South
2023-01-03,Monitor,1,300.00,East
2023-01-04,Laptop,1,1200.00,West
2023-01-05,Mouse,NA,25.50,North
2023-01-05,Keyboard,2,75.00,South
2023-01-06,Laptop,1,1200.00,East
2023-01-07,Monitor,2,300.00,West
2023-01-08,Mouse,3,25.50,North
2023-01-09,Keyboard,NA,75.00,South
2023-01-10,Laptop,1,1200.00,East
2023-01-11,Webcam,4,50.00,North
2023-01-12,Headphones,2,150.00,South
2023-01-13,Webcam,1,50.00,East
2023-01-14,Headphones,3,150.00,West
2023-01-15,Laptop,1,1200.00,North
2023-01-16,Mouse,5,25.50,South
2023-01-17,Keyboard,2,75.00,East
2023-01-18,Monitor,1,300.00,West
2023-01-19,Laptop,1,1200.00,North
2023-01-20,Mouse,3,25.50,South
2023-01-21,Keyboard,2,75.00,East
2023-01-22,Monitor,1,300.00,West
"""

# Use io.StringIO to simulate reading from a file
df = pd.read_csv(io.StringIO(csv_data))

print("--- Original Data Head ---")
print(df.head())
print("\n--- Original Data Info ---")
print(df.info())
print("\n--- Original Data Missing Values ---")
print(df.isnull().sum())

# --- 2. Data Cleaning ---

# Handle missing 'Quantity' values: Fill with median or mean, or drop rows.
# For simplicity, let's fill with the median quantity.
# First, convert 'Quantity' to numeric, coercing errors to NaN.
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
median_quantity = df['Quantity'].median()
df['Quantity'].fillna(median_quantity, inplace=True)
print(f"\nFilled missing 'Quantity' with median: {median_quantity}")

# Convert 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])
print("\n'Date' column converted to datetime.")

# Ensure 'Price' is numeric (it should be if loaded correctly, but good to check)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
# Drop rows where 'Price' might have become NaN due to non-numeric entries
df.dropna(subset=['Price'], inplace=True)
print("\n'Price' column ensured to be numeric.")

# Remove duplicate rows if any (based on all columns)
initial_rows = len(df)
df.drop_duplicates(inplace=True)
if len(df) < initial_rows:
    print(f"\nRemoved {initial_rows - len(df)} duplicate rows.")

print("\n--- Cleaned Data Info ---")
print(df.info())
print("\n--- Cleaned Data Missing Values ---")
print(df.isnull().sum())

# --- 3. Data Exploration and Analysis ---

# Calculate Total Sales for each transaction
df['Total Sales'] = df['Quantity'] * df['Price']
print("\n--- Data Head with 'Total Sales' ---")
print(df.head())

# Overall Total Sales
overall_total_sales = df['Total Sales'].sum()
print(f"\nOverall Total Sales: ${overall_total_sales:,.2f}")

# Sales by Product
sales_by_product = df.groupby('Product')['Total Sales'].sum().sort_values(ascending=False)
print("\n--- Sales by Product ---")
print(sales_by_product)

# Sales by Region
sales_by_region = df.groupby('Region')['Total Sales'].sum().sort_values(ascending=False)
print("\n--- Sales by Region ---")
print(sales_by_region)

# Sales over Time (daily sales)
daily_sales = df.groupby('Date')['Total Sales'].sum()
print("\n--- Daily Sales (first 5 entries) ---")
print(daily_sales.head())

# --- 4. Data Visualization ---

# Set a style for the plots
plt.style.use('seaborn-v0_8-darkgrid')

# Plot 1: Total Sales Over Time
plt.figure(figsize=(12, 6))
daily_sales.plot(kind='line', marker='o', linestyle='-', color='skyblue')
plt.title('Daily Total Sales Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 2: Top 5 Products by Sales
plt.figure(figsize=(10, 7))
top_5_products = sales_by_product.head(5)
top_5_products.plot(kind='bar', color='lightcoral')
plt.title('Top 5 Products by Total Sales', fontsize=16)
plt.xlabel('Product', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.xticks(rotation=45, ha='right') # Rotate labels for better readability
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Plot 3: Sales by Region
plt.figure(figsize=(9, 6))
sales_by_region.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title('Total Sales by Region', fontsize=16)
plt.ylabel('') # Hide the default 'Total Sales' label for pie chart
plt.tight_layout()
plt.show()

print("\n--- Analysis Complete ---")