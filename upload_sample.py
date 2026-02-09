#!/usr/bin/env python3
"""
Upload sample data to the database
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

def upload_sample_data():
    """Upload sample CSV data to database"""
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
        
        # Read CSV data
        print("📁 Reading sample data...")
        df = pd.read_csv('sample_data.csv')
        print(f"📊 Found {len(df)} transactions")
        
        # Upload to raw_transactions table
        print("📤 Uploading to database...")
        df.to_sql('raw_transactions', con=engine, if_exists='append', index=False)
        
        # Process and upload to transactions table
        print("🔄 Processing transactions...")
        
        with engine.connect() as conn:
            for _, row in df.iterrows():
                if row['Status'] == 'Reconciled':
                    conn.execute(text("""
                        INSERT INTO transactions (type, date, item, amount, currency, category, account, status)
                        VALUES (:type, :date, :item, :amount, :currency, :category, :account, :status)
                    """), {
                        'type': row['Type'],
                        'date': row['Date'],
                        'item': row['Name'],
                        'amount': row['Amount'],
                        'currency': row['Currency'],
                        'category': row['Category'],
                        'account': row['Account'],
                        'status': row['Status']
                    })
            
            conn.commit()
        
        print("✅ Sample data uploaded successfully!")
        
        # Show summary
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM transactions"))
            count = result.fetchone()[0]
            print(f"📈 Total transactions in database: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading data: {e}")
        return False

if __name__ == "__main__":
    upload_sample_data()
