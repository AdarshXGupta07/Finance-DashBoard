#!/usr/bin/env python3
"""
Debug the transform function
"""

import pandas as pd
import sys
import os
sys.path.append('scripts')

from database_mysql import extract, transform

def debug_transform():
    try:
        print("🔍 Debugging transform function...")
        
        # Extract data
        df = extract('sample_data.csv')
        print(f"📊 Extracted DataFrame shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Check required columns
        required_cols = ['Type', 'Date', 'Name', 'Amount', 'Currency', 'Category', 'Account', 'Status']
        print(f"🔍 Required columns: {required_cols}")
        print(f"📋 Available columns: {list(df.columns)}")
        
        missing = set(required_cols) - set(df.columns)
        if missing:
            print(f"❌ Missing columns: {missing}")
            return False
        else:
            print("✅ All required columns present!")
        
        # Transform data
        transformed_df = transform(df)
        print(f"✅ Transform successful! New shape: {transformed_df.shape}")
        print(f"📋 New columns: {list(transformed_df.columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    debug_transform()
