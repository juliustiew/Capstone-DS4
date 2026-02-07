#!/usr/bin/env python3
"""
Convert SGJobData.csv to Parquet format for improved performance.
Parquet format provides compression and faster I/O for Streamlit.
"""

import pandas as pd
import os
from pathlib import Path

def convert_csv_to_parquet():
    """Convert CSV to Parquet format with compression."""
    
    csv_path = "/home/julius/SGJobData.csv"
    parquet_path = "/home/julius/SGJobData.parquet"
    
    print(f"📊 Starting CSV to Parquet conversion...")
    print(f"Source: {csv_path}")
    print(f"Target: {parquet_path}")
    
    # Check if source file exists
    if not os.path.exists(csv_path):
        print(f"❌ Error: CSV file not found at {csv_path}")
        return False
    
    # Get original file size
    csv_size = os.path.getsize(csv_path) / (1024**2)  # Convert to MB
    print(f"\n📁 Original CSV size: {csv_size:.2f} MB")
    
    try:
        # Read CSV with same parameters as dashboard
        print("\n⏳ Reading CSV file (this may take a moment)...")
        df = pd.read_csv(csv_path, on_bad_lines='skip', encoding='utf-8')
        print(f"✓ Loaded {len(df):,} rows and {len(df.columns)} columns")
        
        # Convert to Parquet with snappy compression
        print("\n⏳ Writing to Parquet format with snappy compression...")
        df.to_parquet(parquet_path, index=False, compression='snappy', engine='pyarrow')
        print("✓ Parquet file created successfully")
        
        # Get new file size
        parquet_size = os.path.getsize(parquet_path) / (1024**2)  # Convert to MB
        compression_ratio = ((csv_size - parquet_size) / csv_size) * 100
        
        print(f"\n📊 File Size Comparison:")
        print(f"  CSV:     {csv_size:.2f} MB")
        print(f"  Parquet: {parquet_size:.2f} MB")
        print(f"  Reduction: {compression_ratio:.1f}% ({csv_size - parquet_size:.2f} MB saved)")
        
        print("\n✅ Conversion completed successfully!")
        print(f"\nNext step: Update SGJOB_Dashboard.py to use the Parquet file")
        return True
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False

if __name__ == "__main__":
    convert_csv_to_parquet()
