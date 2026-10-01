import pandas as pd

file_names = ["customers", "geolocation", "order_items", "order_payments", "order_reviews", "orders", "products", "sellers"]

for file in file_names:
    df = pd.read_csv(r"C:\Users\mahgo\OneDrive\Desktop\weekly-de-project\data\raw\olist_" + file + "_dataset.csv")
    print("File name: " + file)
    print("Missing values: ")
    print(df.isna().sum())
    print("\n")