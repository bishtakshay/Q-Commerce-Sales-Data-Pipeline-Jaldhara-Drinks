import pandas as pd
import matplotlib.pyplot as plt

# 1oi. Load the CSV
df = pd.read_csv("BB-raw.csv")

# 2. Data Cleaning - Convert numeric columns
cols_to_fix = ['total_quantity', 'total_mrp', 'total_sales']
for col in cols_to_fix:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)


"""
Author: Nikhil
Date: 12-02-2026
Description: This script is used to clean the data in the CSV file.
"""
