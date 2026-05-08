# Here I want to store the credentials for the database connection which is azure sql database. I will use the pyodbc library to connect to the database and execute queries.
import pyodbc
import os

def get_db_connection():
    try:
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE_NAME")
        username = os.getenv("SQL_USERNAME")
        password = os.getenv("SQL_PASWORD")
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e

    