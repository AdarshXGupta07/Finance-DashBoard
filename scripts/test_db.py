from database_sqlite import get_sqlite_connection, load
import os
import pandas as pd
from sqlalchemy import create_engine, text

def test_database_connection():
    print("=== Database Connection Test ===")
    
    # Check database connection
    conn_uri = get_sqlite_connection()
    print(f"Database connection URI: {conn_uri}")
    
    # Check if database file exists
    db_path = "personal_finance_dashboard.db"
    if os.path.exists(db_path):
        print(f"✅ Database file exists: {db_path}")
        size = os.path.getsize(db_path)
        print(f"📁 Database file size: {size} bytes")
    else:
        print("❌ Database file does not exist yet")
    
    # Test database engine
    try:
        engine = create_engine(conn_uri)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            print(f"📊 Tables in database: {tables}")
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_data_loading():
    print("\n=== Data Loading Test ===")
    
    try:
        # Load sample data
        sample_df = pd.read_csv("../sample_transactions.csv")
        print(f"📋 Sample data shape: {sample_df.shape}")
        load(sample_df, "transactions")
        print("✅ Sample data loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def test_queries():
    print("\n=== Query Test ===")
    
    try:
        from read_queries_sqlite import query
        
        # Test basic query
        result = query("transactions")
        print(f"📊 Query result shape: {result.shape}")
        print(f"📋 Columns: {list(result.columns)}")
        print("✅ Queries working successfully!")
        return True
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Personal Finance Dashboard Database Connection")
    print("=" * 60)
    
    # Run all tests
    db_ok = test_database_connection()
    data_ok = test_data_loading()
    query_ok = test_queries()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Database Connection: {'✅ OK' if db_ok else '❌ FAILED'}")
    print(f"Data Loading: {'✅ OK' if data_ok else '❌ FAILED'}")
    print(f"Queries: {'✅ OK' if query_ok else '❌ FAILED'}")
    
    if db_ok and data_ok and query_ok:
        print("\n🎉 All database tests passed! SQLite is properly connected.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
