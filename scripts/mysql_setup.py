#!/usr/bin/env python3
"""
MySQL Database Setup Script for Personal Finance Dashboard
This script creates the database, user, and initializes the schema
"""

import os
import sys
import getpass
from sqlalchemy import create_engine, text
import pymysql
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

def get_root_connection():
    """Get MySQL root connection for database setup"""
    print("MySQL Root Connection Required")
    print("=" * 40)
    
    host = input(f"Enter MySQL host (default: {os.getenv('MYSQL_HOST', 'localhost')}): ") or os.getenv('MYSQL_HOST', 'localhost')
    port = input(f"Enter MySQL port (default: {os.getenv('MYSQL_PORT', '3306')}): ") or os.getenv('MYSQL_PORT', '3306')
    root_user = input("Enter MySQL root username (default: root): ") or "root"
    root_password = getpass.getpass("Enter MySQL root password: ")
    
    try:
        # URL-encode the password to handle special characters
        encoded_password = quote_plus(root_password)
        connection_string = f"mysql+pymysql://{root_user}:{encoded_password}@{host}:{port}/mysql"
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Root connection successful!")
        return engine, root_password
    except Exception as e:
        print(f"❌ Root connection failed: {e}")
        return None, None

def create_database_and_user(engine, root_password):
    """Create database and user for the finance dashboard"""
    db_name = os.getenv('MYSQL_DATABASE', 'personal_finance_dashboard')
    app_user = os.getenv('MYSQL_USER', 'finance_user')
    
    # Get password for application user (use from env or prompt)
    app_password = os.getenv('MYSQL_PASSWORD')
    if not app_password:
        app_password = getpass.getpass(f"Enter password for {app_user} (leave empty for auto-generated): ")
    
    if not app_password:
        import secrets
        import string
        app_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        print(f"🔑 Generated password for {app_user}: {app_password}")
    
    try:
        with engine.connect() as conn:
            # Create database
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"✅ Database '{db_name}' created successfully!")
            
            # Create user
            conn.execute(text(f"DROP USER IF EXISTS '{app_user}'@'localhost'"))
            conn.execute(text(f"CREATE USER '{app_user}'@'localhost' IDENTIFIED BY '{app_password}'"))
            print(f"✅ User '{app_user}' created successfully!")
            
            # Grant privileges
            conn.execute(text(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{app_user}'@'localhost'"))
            conn.execute(text("FLUSH PRIVILEGES"))
            print(f"✅ Privileges granted to '{app_user}'!")
            
        return app_password
    except Exception as e:
        print(f"❌ Error creating database/user: {e}")
        return None

def create_tables(engine):
    """Create the necessary tables for the finance dashboard"""
    try:
        with engine.connect() as conn:
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # Create transactions table (processed data)
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_date (date),
                    INDEX idx_category (category),
                    INDEX idx_account (account),
                    INDEX idx_type (type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # Create categories table for reference
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    type ENUM('Income', 'Expense', 'Both') DEFAULT 'Both',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # Create accounts table for reference
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    type ENUM('Asset', 'Liability', 'Equity') DEFAULT 'Asset',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            print("✅ Tables created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

def insert_default_data(engine):
    """Insert default categories and accounts"""
    try:
        with engine.connect() as conn:
            # Default categories
            default_categories = [
                ('Food & Dining', 'Expense', 'Restaurants, groceries, food delivery'),
                ('Transportation', 'Expense', 'Gas, public transport, ride-sharing'),
                ('Shopping', 'Expense', 'Clothing, electronics, household items'),
                ('Entertainment', 'Expense', 'Movies, games, subscriptions'),
                ('Bills & Utilities', 'Expense', 'Electricity, water, internet, phone'),
                ('Healthcare', 'Expense', 'Medicine, doctor visits, insurance'),
                ('Education', 'Expense', 'Tuition, books, courses'),
                ('Salary', 'Income', 'Monthly salary and wages'),
                ('Freelance', 'Income', 'Freelance work and side gigs'),
                ('Investments', 'Income', 'Dividends, interest, capital gains'),
                ('Transfer', 'Both', 'Money transfers between accounts')
            ]
            
            for cat_name, cat_type, description in default_categories:
                conn.execute(text("""
                    INSERT IGNORE INTO categories (name, type, description) 
                    VALUES (:name, :type, :description)
                """), {"name": cat_name, "type": cat_type, "description": description})
            
            # Default accounts
            default_accounts = [
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
                ('SLoan', 'Liability', 'Shopee loan'),
                ('Binance', 'Asset', 'Binance crypto account'),
                ('Ronin', 'Asset', 'Ronin wallet for gaming'),
                ('BDO', 'Asset', 'BDO account'),
                ('BPI', 'Asset', 'BPI account'),
                ('Borrowed Money', 'Liability', 'Money borrowed from others'),
                ('Loaned Money', 'Asset', 'Money loaned to others'),
                ('School Loans', 'Liability', 'Educational loans')
            ]
            
            for acc_name, acc_type, description in default_accounts:
                conn.execute(text("""
                    INSERT IGNORE INTO accounts (name, type, description) 
                    VALUES (:name, :type, :description)
                """), {"name": acc_name, "type": acc_type, "description": description})
            
            print("✅ Default data inserted successfully!")
            
    except Exception as e:
        print(f"❌ Error inserting default data: {e}")
        return False
    
    return True

def create_env_file(app_password):
    """Create .env file with database credentials"""
    env_content = f"""# MySQL Database Configuration
MYSQL_USER=finance_user
MYSQL_PASSWORD={app_password}
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=personal_finance_dashboard

# Application Settings
APP_ENV=production
DEBUG=False
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Please keep this file secure and do not commit to version control")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def main():
    print("Personal Finance Dashboard - MySQL Setup")
    print("=" * 50)
    
    # Get root connection
    engine, root_password = get_root_connection()
    if not engine:
        sys.exit(1)
    
    # Create database and user
    app_password = create_database_and_user(engine, root_password)
    if not app_password:
        sys.exit(1)
    
    # Connect to the new database
    try:
        # Use environment variables for database connection
        db_user = os.getenv('MYSQL_USER', 'finance_user')
        db_password = app_password  # Use the password from create_database_and_user
        db_host = os.getenv('MYSQL_HOST', 'localhost')
        db_port = os.getenv('MYSQL_PORT', '3306')
        db_name = os.getenv('MYSQL_DATABASE', 'personal_finance_dashboard')
        
        # URL-encode the password
        encoded_password = quote_plus(db_password)
        connection_string = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
        db_engine = create_engine(connection_string)
        
        # Create tables
        if not create_tables(db_engine):
            sys.exit(1)
        
        # Insert default data
        if not insert_default_data(db_engine):
            sys.exit(1)
        
        # Create .env file
        create_env_file(app_password)
        
        print("\n" + "=" * 50)
        print("🎉 MySQL setup completed successfully!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: streamlit run scripts/app_mysql.py")
        print("3. Open browser to: http://localhost:8501")
        print("\nYour database is ready to use!")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
