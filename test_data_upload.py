#!/usr/bin/env python3
"""
Test data upload functionality
"""

import pandas as pd
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

def test_data_upload():
    """Test uploading data through the app's data upload functionality"""
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
        
        # Test the transform and load functions
        sys.path.append('scripts')
        from database_mysql import extract, transform, load
        
        print("🔍 Testing data upload process...")
        
        # Extract
        df = extract('sample_data.csv')
        print(f"✅ Extract successful: {len(df)} rows")
        
        # Transform
        transformed_df = transform(df)
        print(f"✅ Transform successful: {len(transformed_df)} rows")
        
        # Load to raw_transactions
        load(transformed_df, 'raw_transactions_test', connection_string)
        print("✅ Load to raw_transactions_test successful")
        
        # Test manual insert to transactions table
        with engine.connect() as conn:
            for _, row in transformed_df.iterrows():
                conn.execute(text("""
                    INSERT IGNORE INTO transactions (type, date, item, amount, currency, category, account, status)
                    VALUES (:type, :date, :item, :amount, :currency, :category, :account, :status)
                """), {
                    'type': row['type'],
                    'date': row['date'],
                    'item': row['item'],
                    'amount': row['amount'],
                    'currency': row['currency'],
                    'category': row['category'],
                    'account': row['account'],
                    'status': row['status']
                })
            conn.commit()
        
        print("✅ Manual insert to transactions successful")
        
        # Verify data
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM transactions"))
            count = result.fetchone()[0]
            print(f"📊 Total transactions in database: {count}")
        
        print("🎉 Data upload test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in data upload test: {e}")
        return False

if __name__ == "__main__":
    test_data_upload()
