#!/usr/bin/env python3
"""
Data Upload Manager for Personal Finance Dashboard
This script handles CSV data uploads, validation, and database insertion
"""

import os
import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from database_mysql import get_mysql_connection, extract, transform, load
import warnings
warnings.filterwarnings('ignore')

class DataUploadManager:
    def __init__(self):
        self.engine = None
        self.required_columns = ['Type', 'Date', 'Name', 'Amount', 'Currency', 'Category', 'Account', 'Status']
        self.valid_types = ['Income', 'Expense', 'Transfer']
        self.valid_statuses = ['Reconciled', 'Pending', 'Cleared']
        
    def connect_to_database(self):
        """Establish database connection"""
        try:
            connection_uri = get_mysql_connection()
            self.engine = create_engine(connection_uri)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            print("✅ Database connection successful!")
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def validate_csv_structure(self, file_path):
        """Validate CSV file structure"""
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            print(f"📊 CSV loaded: {len(df)} rows, {len(df.columns)} columns")
            
            # Check required columns
            missing_columns = set(self.required_columns) - set(df.columns)
            if missing_columns:
                print(f"❌ Missing required columns: {missing_columns}")
                return False, df
            
            print("✅ All required columns present")
            return True, df
            
        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")
            return False, None
    
    def validate_data_content(self, df):
        """Validate data content and quality"""
        issues = []
        warnings_list = []
        
        # Check for empty data
        if df.empty:
            issues.append("CSV file is empty")
            return False, issues, warnings_list
        
        # Check data types and values
        for index, row in df.iterrows():
            row_num = index + 2  # CSV row numbers start at 2 (after header)
            
            # Validate Type
            if pd.isna(row['Type']) or row['Type'] not in self.valid_types:
                issues.append(f"Row {row_num}: Invalid Type '{row.get('Type', 'missing')}'")
            
            # Validate Date
            try:
                if pd.notna(row['Date']):
                    pd.to_datetime(row['Date'])
                else:
                    issues.append(f"Row {row_num}: Missing Date")
            except:
                issues.append(f"Row {row_num}: Invalid Date format '{row['Date']}'")
            
            # Validate Amount
            try:
                if pd.notna(row['Amount']):
                    float(row['Amount'])
                else:
                    issues.append(f"Row {row_num}: Missing Amount")
            except:
                issues.append(f"Row {row_num}: Invalid Amount '{row['Amount']}'")
            
            # Validate required string fields
            for field in ['Name', 'Category', 'Account']:
                if pd.isna(row[field]) or str(row[field]).strip() == '':
                    issues.append(f"Row {row_num}: Missing {field}")
            
            # Validate Status
            if pd.notna(row['Status']) and row['Status'] not in self.valid_statuses:
                warnings_list.append(f"Row {row_num}: Unusual Status '{row['Status']}'")
        
        # Check for duplicates
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            warnings_list.append(f"Found {duplicate_count} duplicate rows")
        
        # Summary statistics
        print(f"\n📈 Data Validation Summary:")
        print(f"  Total rows: {len(df)}")
        print(f"  Valid types: {df['Type'].value_counts().to_dict()}")
        print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"  Total amount: {df['Amount'].sum():.2f}")
        
        return len(issues) == 0, issues, warnings_list
    
    def clean_and_transform_data(self, df):
        """Clean and transform data for database insertion"""
        try:
            # Make a copy to avoid modifying original
            cleaned_df = df.copy()
            
            # Convert Date column
            cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date'])
            
            # Convert Amount to numeric
            cleaned_df['Amount'] = pd.to_numeric(cleaned_df['Amount'], errors='coerce')
            
            # Clean string columns
            string_columns = ['Type', 'Name', 'Currency', 'Category', 'Account', 'Status']
            for col in string_columns:
                cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            
            # Filter for reconciled transactions (as per original logic)
            reconciled_df = cleaned_df[cleaned_df['Status'] == 'Reconciled'].copy()
            
            print(f"🧹 Data cleaning completed:")
            print(f"  Original rows: {len(df)}")
            print(f"  After cleaning: {len(cleaned_df)}")
            print(f"  Reconciled only: {len(reconciled_df)}")
            
            return reconciled_df
            
        except Exception as e:
            print(f"❌ Error during data cleaning: {e}")
            return None
    
    def preview_data(self, df, max_rows=10):
        """Preview data before upload"""
        print(f"\n👀 Data Preview (showing first {max_rows} rows):")
        print("-" * 80)
        
        # Format for display
        display_df = df.head(max_rows).copy()
        
        # Format date and amount for better readability
        if 'Date' in display_df.columns:
            display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        if 'Amount' in display_df.columns:
            display_df['Amount'] = display_df['Amount'].apply(lambda x: f"{x:,.2f}")
        
        print(display_df.to_string(index=False))
        
        if len(df) > max_rows:
            print(f"... and {len(df) - max_rows} more rows")
    
    def upload_to_database(self, df, table_name='raw_transactions', mode='append'):
        """Upload data to database"""
        try:
            if not self.engine:
                if not self.connect_to_database():
                    return False
            
            # Determine upload mode
            if_exists = 'append' if mode == 'append' else 'replace'
            
            # Upload data
            rows_uploaded = df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False,
                chunksize=1000
            )
            
            print(f"✅ Successfully uploaded {rows_uploaded} rows to '{table_name}' table")
            
            # Update transactions table if uploading raw_transactions
            if table_name == 'raw_transactions':
                self.update_transactions_table()
            
            return True
            
        except Exception as e:
            print(f"❌ Error uploading to database: {e}")
            return False
    
    def update_transactions_table(self):
        """Update the processed transactions table from raw_transactions"""
        try:
            with self.engine.connect() as conn:
                # Clear existing transactions
                conn.execute(text("DELETE FROM transactions"))
                
                # Insert processed data
                conn.execute(text("""
                    INSERT INTO transactions (type, date, item, amount, currency, category, account, status)
                    SELECT 
                        Type as type,
                        Date as date,
                        Name as item,
                        Amount as amount,
                        Currency as currency,
                        Category as category,
                        Account as account,
                        Status as status
                    FROM raw_transactions
                    WHERE Status = 'Reconciled'
                """))
                
                conn.commit()
                print("✅ Transactions table updated successfully!")
                
        except Exception as e:
            print(f"❌ Error updating transactions table: {e}")
    
    def get_upload_history(self):
        """Get history of data uploads"""
        try:
            if not self.engine:
                if not self.connect_to_database():
                    return None
            
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT 
                        DATE(created_at) as upload_date,
                        COUNT(*) as records_count,
                        COUNT(DISTINCT category) as categories_count,
                        COUNT(DISTINCT account) as accounts_count,
                        SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) as total_income,
                        SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) as total_expenses
                    FROM transactions
                    GROUP BY DATE(created_at)
                    ORDER BY upload_date DESC
                    LIMIT 10
                """))
                
                return result.fetchall()
                
        except Exception as e:
            print(f"❌ Error getting upload history: {e}")
            return None
    
    def export_data(self, table_name='transactions', output_file=None):
        """Export data to CSV"""
        try:
            if not self.engine:
                if not self.connect_to_database():
                    return False
            
            # Generate filename if not provided
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"export_{table_name}_{timestamp}.csv"
            
            # Read data from database
            df = pd.read_sql_table(table_name, self.engine)
            
            # Export to CSV
            df.to_csv(output_file, index=False)
            print(f"✅ Data exported to '{output_file}' ({len(df)} rows)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return False

def main():
    print("Personal Finance Dashboard - Data Upload Manager")
    print("=" * 50)
    
    manager = DataUploadManager()
    
    while True:
        print("\n📤 Upload Management Options:")
        print("1. Upload CSV file")
        print("2. Preview upload history")
        print("3. Export data to CSV")
        print("4. Test database connection")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            file_path = input("Enter CSV file path: ").strip()
            
            if not os.path.exists(file_path):
                print(f"❌ File '{file_path}' not found")
                continue
            
            print(f"\n📁 Processing file: {file_path}")
            
            # Validate structure
            valid, df = manager.validate_csv_structure(file_path)
            if not valid:
                continue
            
            # Validate content
            valid, issues, warnings_list = manager.validate_data_content(df)
            
            if issues:
                print("\n❌ Validation Issues Found:")
                for issue in issues[:10]:  # Show first 10 issues
                    print(f"  • {issue}")
                if len(issues) > 10:
                    print(f"  ... and {len(issues) - 10} more issues")
                continue
            
            if warnings_list:
                print("\n⚠️  Warnings:")
                for warning in warnings_list[:5]:  # Show first 5 warnings
                    print(f"  • {warning}")
                if len(warnings_list) > 5:
                    print(f"  ... and {len(warnings_list) - 5} more warnings")
            
            # Preview data
            manager.preview_data(df)
            
            # Confirm upload
            confirm = input("\n📤 Proceed with upload? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("❌ Upload cancelled")
                continue
            
            # Clean and upload
            cleaned_df = manager.clean_and_transform_data(df)
            if cleaned_df is not None:
                mode = input("Upload mode (append/replace) [default: append]: ").strip() or 'append'
                if manager.upload_to_database(cleaned_df, mode=mode):
                    print("🎉 Upload completed successfully!")
        
        elif choice == '2':
            history = manager.get_upload_history()
            if history:
                print("\n📊 Upload History:")
                print("-" * 70)
                print(f"{'Date':<12} {'Records':<10} {'Categories':<12} {'Accounts':<10} {'Income':<12} {'Expenses':<12}")
                print("-" * 70)
                for row in history:
                    print(f"{row[0]:<12} {row[1]:<10} {row[2]:<12} {row[3]:<10} {row[4]:<12.2f} {row[5]:<12.2f}")
            else:
                print("📭 No upload history found")
        
        elif choice == '3':
            table = input("Table name (transactions/raw_transactions) [default: transactions]: ").strip() or 'transactions'
            filename = input("Output filename (leave empty for auto-generated): ").strip() or None
            manager.export_data(table, filename)
        
        elif choice == '4':
            manager.connect_to_database()
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
