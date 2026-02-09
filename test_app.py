#!/usr/bin/env python3
"""
Test the MySQL database connection and data
"""

import sys
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

def load_env_directly():
    """Load environment variables directly from .env file"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key] = value
        return env_vars
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return None

def test_database():
    """Test database and show sample data"""
    env_vars = load_env_directly()
    if not env_vars:
        return False
    
    try:
        # Get connection details
        user = env_vars.get('MYSQL_USER', 'finance_user')
        password = env_vars.get('MYSQL_PASSWORD', '')
        host = env_vars.get('MYSQL_HOST', 'localhost')
        port = env_vars.get('MYSQL_PORT', '3306')
        database = env_vars.get('MYSQL_DATABASE', 'personal_finance_dashboard')
        
        # URL-encode password
        encoded_password = quote_plus(password)
        connection_string = f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"
        
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            # Check tables
            print("📊 Database Tables:")
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            for table in tables:
                print(f"  ✓ {table[0]}")
            
            # Check categories
            print("\n🏷️  Categories:")
            result = conn.execute(text("SELECT name, type FROM categories LIMIT 5"))
            categories = result.fetchall()
            for cat in categories:
                print(f"  • {cat[0]} ({cat[1]})")
            
            # Check accounts
            print("\n💳 Accounts:")
            result = conn.execute(text("SELECT name, type FROM accounts LIMIT 5"))
            accounts = result.fetchall()
            for acc in accounts:
                print(f"  • {acc[0]} ({acc[1]})")
            
            # Check if we have any transactions
            result = conn.execute(text("SELECT COUNT(*) FROM transactions"))
            count = result.fetchone()[0]
            print(f"\n📈 Transactions: {count}")
            
            print("\n✅ Database is ready for use!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_database()
