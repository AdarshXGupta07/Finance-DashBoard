import pandas as pd
from sqlalchemy import create_engine, text
import os

def get_mysql_connection():
    """Create MySQL database connection"""
    # Default MySQL connection settings - update these with your actual MySQL credentials
    db_user = os.getenv('MYSQL_USER', 'root')
    db_password = os.getenv('MYSQL_PASSWORD', '')
    db_host = os.getenv('MYSQL_HOST', 'localhost')
    db_port = os.getenv('MYSQL_PORT', '3306')
    db_name = os.getenv('MYSQL_DATABASE', 'personal_finance_dashboard')
    
    return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def extract(file):
    """
    Reads a CSV file and returns a DataFrame.
    """
    try:
        raw_transactions = pd.read_csv(file)
        return raw_transactions
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame()

def transform(df):
    """
    Cleans and transforms the DataFrame for loading.
    """
    col_names = ['Type', 'Date', 'Name', 'Amount', 'Currency', 'Category', 'Account', 'Status']
    if not set(col_names).issubset(df.columns):
        raise ValueError(f"Missing columns in input DataFrame: {set(col_names) - set(df.columns)}")
    cleaned_df = df.loc[df['Status'] == 'Reconciled', col_names]
    new_col_names = ['type', 'date', 'item', 'amount', 'currency', 'category', 'account', 'status']
    cleaned_df.columns = new_col_names
    cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
    return cleaned_df

def load(df, db_table, connection_uri=None):
    """
    Loads the DataFrame into the specified database table.
    """
    if connection_uri is None:
        connection_uri = get_mysql_connection()
    
    db_engine = create_engine(connection_uri)
    try:
        df.to_sql(
            name=db_table,
            con=db_engine,
            if_exists="replace",
            index=False
        )
        print(f"Successfully loaded data into {db_table}")
    except Exception as e:
        print(f"Error loading data to database: {e}")

def drop(table, connection_uri=None):
    """
    Drops the specified table from the database if it exists.
    """
    if connection_uri is None:
        connection_uri = get_mysql_connection()
    
    db_engine = create_engine(connection_uri)
    try:
        with db_engine.connect() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table};"))
            connection.commit()
        print(f"Successfully dropped table {table}")
    except Exception as e:
        print(f"Error dropping table: {e}")

def create_database(connection_uri=None):
    """
    Creates the database if it doesn't exist.
    """
    if connection_uri is None:
        connection_uri = get_mysql_connection()
    
    # Remove database name from connection URI to connect to MySQL server
    base_uri = connection_uri.rsplit('/', 1)[0]
    db_engine = create_engine(base_uri)
    
    try:
        with db_engine.connect() as connection:
            connection.execute(text("CREATE DATABASE IF NOT EXISTS personal_finance_dashboard"))
            connection.commit()
        print("Database created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
