#!/usr/bin/env python3
"""
Simple MySQL Setup Script
Direct approach without complex environment variable handling
"""

import os
import sys
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

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
    except FileNotFoundError:
        print("❌ .env file not found!")
        return None
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return None

def test_mysql_connection():
    """Test MySQL connection using .env credentials"""
    env_vars = load_env_directly()
    if not env_vars:
        return False, None, None
    
    try:
        # Get connection details from .env
        user = env_vars.get('MYSQL_USER', 'finance_user')
        password = env_vars.get('MYSQL_PASSWORD', '')
        host = env_vars.get('MYSQL_HOST', 'localhost')
        port = env_vars.get('MYSQL_PORT', '3306')
        database = env_vars.get('MYSQL_DATABASE', 'personal_finance_dashboard')
        
        # URL-encode password for special characters
        encoded_password = quote_plus(password)
        connection_string = f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"
        
        print(f"🔍 Testing connection to {database}...")
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.fetchone()[0] == 1:
                print("✅ Connection successful!")
                return True, engine, env_vars
            else:
                print("❌ Connection test failed")
                return False, None, None
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False, None, None

def create_database_tables(engine):
    """Create database tables"""
    try:
        print("📊 Creating database tables...")
        
        with engine.connect() as conn:
            # Create categories table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    type ENUM('Income', 'Expense', 'Both') DEFAULT 'Both',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """))
            
            # Create accounts table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    type ENUM('Asset', 'Liability', 'Equity') DEFAULT 'Asset',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """))
            
            # Create raw_transactions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS raw_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    Type VARCHAR(50),
                    Date DATE,
                    Name VARCHAR(255),
                    Amount DECIMAL(15, 2),
                    Currency VARCHAR(10),
                    Category VARCHAR(100),
                    Account VARCHAR(100),
                    Status VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """))
            
            # Create transactions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    type ENUM('Income', 'Expense', 'Transfer') NOT NULL,
                    date DATE NOT NULL,
                    item VARCHAR(255) NOT NULL,
                    amount DECIMAL(15, 2) NOT NULL,
                    currency VARCHAR(10) DEFAULT 'PHP',
                    category VARCHAR(100) NOT NULL,
                    account VARCHAR(100) NOT NULL,
                    status VARCHAR(50) DEFAULT 'Reconciled',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """))
            
            conn.commit()
            print("✅ Tables created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def insert_default_data(engine):
    """Insert default categories and accounts"""
    try:
        print("📝 Inserting default data...")
        
        with engine.connect() as conn:
            # Default categories
            categories = [
                ('Food & Dining', 'Expense', 'Restaurants, groceries, food delivery'),
                ('Transportation', 'Expense', 'Gas, public transport, ride-sharing'),
                ('Shopping', 'Expense', 'Clothing, electronics, household items'),
                ('Entertainment', 'Expense', 'Movies, games, subscriptions'),
                ('Bills & Utilities', 'Expense', 'Electricity, water, internet, phone'),
                ('Healthcare', 'Expense', 'Medicine, doctor visits, insurance'),
                ('Salary', 'Income', 'Monthly salary and wages'),
                ('Freelance', 'Income', 'Freelance work and side gigs'),
                ('Investments', 'Income', 'Dividends, interest, capital gains'),
                ('Transfer', 'Both', 'Money transfers between accounts')
            ]
            
            for cat_name, cat_type, description in categories:
                conn.execute(text("""
                    INSERT IGNORE INTO categories (name, type, description) 
                    VALUES (:name, :type, :description)
                """), {"name": cat_name, "type": cat_type, "description": description})
            
            # Default accounts
            accounts = [
                ('Wallet', 'Asset', 'Physical cash and wallet'),
                ('Union Bank', 'Asset', 'Union Bank account'),
                ('SeaBank', 'Asset', 'SeaBank account'),
                ('SeaBank Credit', 'Liability', 'SeaBank credit card'),
                ('GCash', 'Asset', 'GCash e-wallet'),
                ('Maya', 'Asset', 'Maya e-wallet'),
                ('Maya Easy Credit', 'Liability', 'Maya credit line'),
                ('GrabPay', 'Asset', 'GrabPay e-wallet'),
                ('ShopeePay', 'Asset', 'ShopeePay e-wallet'),
                ('SPayLater', 'Liability', 'ShopeePay credit'),
                ('BDO', 'Asset', 'BDO account'),
                ('BPI', 'Asset', 'BPI account'),
                ('Borrowed Money', 'Liability', 'Money borrowed from others'),
                ('Loaned Money', 'Asset', 'Money loaned to others'),
                ('School Loans', 'Liability', 'Educational loans')
            ]
            
            for acc_name, acc_type, description in accounts:
                conn.execute(text("""
                    INSERT IGNORE INTO accounts (name, type, description) 
                    VALUES (:name, :type, :description)
                """), {"name": acc_name, "type": acc_type, "description": description})
            
            conn.commit()
            print("✅ Default data inserted successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error inserting default data: {e}")
        return False

def main():
    print("🚀 Simple MySQL Setup for Personal Finance Dashboard")
    print("=" * 60)
    
    # Test connection first
    success, engine, env_vars = test_mysql_connection()
    if not success:
        print("\n❌ Cannot connect to MySQL database!")
        print("Please ensure:")
        print("1. MySQL server is running")
        print("2. Database 'personal_finance_dashboard' exists")
        print("3. User 'finance_user' has correct permissions")
        print("4. .env file contains correct credentials")
        return False
    
    # Create tables
    if not create_database_tables(engine):
        return False
    
    # Insert default data
    if not insert_default_data(engine):
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("Your MySQL database is ready to use!")
    print("\nNext steps:")
    print("1. Run: streamlit run scripts/app_mysql.py")
    print("2. Open browser to: http://localhost:8501")
    
    return True

if __name__ == "__main__":
    main()
