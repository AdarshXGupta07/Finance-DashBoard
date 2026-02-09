#!/usr/bin/env python3
"""
Test script to verify MySQL database connection using .env file
"""

import sys
import os
sys.path.append('scripts')

from database_mysql import get_mysql_connection
from sqlalchemy import create_engine, text

def test_connection():
    try:
        print("🔍 Testing MySQL database connection...")
        
        # Get connection string
        conn_string = get_mysql_connection()
        print(f"📡 Connection string: mysql+pymysql://***:***@{os.getenv('MYSQL_HOST', 'localhost')}:{os.getenv('MYSQL_PORT', '3306')}/{os.getenv('MYSQL_DATABASE', 'personal_finance_dashboard')}")
        
        # Create engine and test connection
        engine = create_engine(conn_string)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database connection test failed")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n🎉 Your MySQL configuration is working!")
        print("You can now run the setup script to create the database.")
    else:
        print("\n⚠️  Please check your MySQL server and credentials.")
