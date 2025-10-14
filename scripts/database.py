import pandas as pd
from sqlalchemy import create_engine, text

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

def load(df, db_table, connection_uri):
    """
    Loads the DataFrame into the specified database table.
    """
    db_engine = create_engine(connection_uri)
    try:
        df.to_sql(
            name=db_table,
            con=db_engine,
            if_exists="replace",
            index=False
        )
    except Exception as e:
        print(f"Error loading data to database: {e}")

def drop(table, connection_uri):
    """
    Drops the specified table from the database if it exists.
    """
    db_engine = create_engine(connection_uri)
    try:
        with db_engine.connect() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table};"))
    except Exception as e:
        print(f"Error dropping table: {e}")