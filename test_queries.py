#!/usr/bin/env python3
"""
Test the MySQL queries
"""

import sys
import os
sys.path.append('scripts')

from read_queries_mysql import query

def test_queries():
    try:
        print("🔍 Testing MySQL queries...")
        
        # Test transactions query
        print("\n📊 Testing transactions query...")
        df = query('transactions')
        print(f"✅ Transactions query successful! Rows: {len(df)}")
        if len(df) > 0:
            print(f"📋 Columns: {list(df.columns)}")
        
        # Test monthly_amount_over_time query
        print("\n📈 Testing monthly_amount_over_time query...")
        df = query('monthly_amount_over_time')
        print(f"✅ Monthly query successful! Rows: {len(df)}")
        
        # Test expenses_per_category query
        print("\n💰 Testing expenses_per_category query...")
        df = query('expenses_per_category')
        print(f"✅ Category expenses query successful! Rows: {len(df)}")
        
        print("\n🎉 All queries working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing queries: {e}")
        return False

if __name__ == "__main__":
    test_queries()
