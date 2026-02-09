import pandas as pd
from sqlalchemy import create_engine
from database_sqlite import get_sqlite_connection

def read_query(query_name):
    with open("queries_sqlite.sql", 'r') as file:
        content = file.read()

    queries = [q.strip() for q in content.split('--@name:')]
    for q in queries:
        lines = q.split('\n', 1)
        name = lines[0].strip()
        query = lines[1].strip() if len(lines) > 1 else ''
        if name == query_name:
            return query

    raise ValueError(f"Query with name '{query_name}' not found in the file.")

def query(query_name):
    connection_uri = get_sqlite_connection()
    query = read_query(query_name)
    db_engine = create_engine(connection_uri)
    try:
        df = pd.read_sql(query, db_engine)
        df.index = range(1, len(df) + 1)
        return df
    except Exception as e:
        print(f"Error executing query {query_name}: {e}")
        return pd.DataFrame()
