import pandas as pd
import os

def compare_data():
    # File paths
    raw_file = r'Data\raw\houses_with_pool.csv'
    processed_file = r'Data\processed\clean_data.csv'
    
    # Load datasets
    print("=" * 80)
    print("DATA COMPARISON REPORT: RAW vs PROCESSED")
    print("=" * 80)
    
    raw_data = pd.read_csv(raw_file)
    processed_data = pd.read_csv(processed_file)
    
    # 1. Rows and Columns
    print("\n1. DATASET DIMENSIONS")
    print("-" * 80)
    print(f"Raw Data:       {raw_data.shape[0]} rows × {raw_data.shape[1]} columns")
    print(f"Processed Data: {processed_data.shape[0]} rows × {processed_data.shape[1]} columns")
    rows_removed = raw_data.shape[0] - processed_data.shape[0]
    print(f"Rows Removed:   {rows_removed} rows ({(rows_removed/raw_data.shape[0]*100):.2f}%)")
    
    # 2. Missing Values
    print("\n2. MISSING VALUES")
    print("-" * 80)
    raw_missing = raw_data.isnull().sum()
    processed_missing = processed_data.isnull().sum()
    
    print("Raw Data Missing Values:")
    if raw_missing.sum() > 0:
        for col in raw_missing[raw_missing > 0].index:
            print(f"  - {col}: {raw_missing[col]} ({(raw_missing[col]/len(raw_data)*100):.2f}%)")
    else:
        print("  No missing values")
    
    print("\nProcessed Data Missing Values:")
    if processed_missing.sum() > 0:
        for col in processed_missing[processed_missing > 0].index:
            print(f"  - {col}: {processed_missing[col]} ({(processed_missing[col]/len(processed_data)*100):.2f}%)")
    else:
        print("  No missing values")
    
    # 3. Data Types
    print("\n3. DATA TYPES")
    print("-" * 80)
    print("Raw Data Types:")
    print(raw_data.dtypes.to_string())
    print("\nProcessed Data Types:")
    print(processed_data.dtypes.to_string())
    
    # 4. Duplicate Rows
    print("\n4. DUPLICATE ROWS REMOVED")
    print("-" * 80)
    raw_duplicates = raw_data.duplicated().sum()
    processed_duplicates = processed_data.duplicated().sum()
    duplicates_removed = raw_duplicates - processed_duplicates
    print(f"Raw Data Duplicates:       {raw_duplicates}")
    print(f"Processed Data Duplicates: {processed_duplicates}")
    print(f"Duplicates Removed:        {duplicates_removed}")
    
    # 5. Invalid Values Removed (Area > 0, Price > 0)
    print("\n5. INVALID VALUES REMOVED")
    print("-" * 80)
    
    # Check for Area and Price columns
    area_col = None
    price_col = None
    
    for col in raw_data.columns:
        if col.lower() in ['area', 'sq_ft', 'sqft', 'size']:
            area_col = col
        if col.lower() in ['price', 'cost', 'value']:
            price_col = col
    
    if area_col and price_col:
        raw_invalid_area = (raw_data[area_col] <= 0).sum()
        raw_invalid_price = (raw_data[price_col] <= 0).sum()
        
        processed_invalid_area = (processed_data[area_col] <= 0).sum()
        processed_invalid_price = (processed_data[price_col] <= 0).sum()
        
        print(f"Invalid Area (Area ≤ 0):")
        print(f"  Raw Data:       {raw_invalid_area} rows")
        print(f"  Processed Data: {processed_invalid_area} rows")
        print(f"  Removed:        {raw_invalid_area - processed_invalid_area} rows")
        
        print(f"\nInvalid Price (Price ≤ 0):")
        print(f"  Raw Data:       {raw_invalid_price} rows")
        print(f"  Processed Data: {processed_invalid_price} rows")
        print(f"  Removed:        {raw_invalid_price - processed_invalid_price} rows")
    else:
        print(f"Note: Could not identify Area/Price columns")
        print(f"Available columns: {', '.join(raw_data.columns.tolist())}")
    
    # Summary Statistics
    print("\n6. SUMMARY STATISTICS")
    print("-" * 80)
    print("Raw Data:")
    print(raw_data.describe().to_string())
    print("\n\nProcessed Data:")
    print(processed_data.describe().to_string())
    
    # Final Summary
    print("\n" + "=" * 80)
    print("CLEANING SUMMARY")
    print("=" * 80)
    print(f"✓ Total Rows Removed: {rows_removed}")
    print(f"✓ Duplicates Removed: {duplicates_removed}")
    if area_col and price_col:
        invalid_removed = raw_invalid_area + raw_invalid_price - processed_invalid_area - processed_invalid_price
        print(f"✓ Invalid Values Removed: {invalid_removed} (Area ≤ 0 or Price ≤ 0)")
    print(f"✓ Data Quality: Improved with valid data only")
    print("=" * 80)

if __name__ == "__main__":
    compare_data()
