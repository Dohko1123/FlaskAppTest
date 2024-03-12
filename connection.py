import os
import pymssql

def first_connection():
    '''
    This function connects to the database and returns the connection object.
    input: None
    output: conn (object): Connection object to the database.'''
    try:
        MSSQL_SERVER ='awaq.database.windows.net'
        MSSQL_DB ='BiologyDB'
        MSSQL_USER ='rootadmin'
        MSSQL_PASSWORD ='Dios123*'

        
        conn = pymssql.connect(server=MSSQL_SERVER,
                            user=MSSQL_USER,
                            password=MSSQL_PASSWORD,
                            database=MSSQL_DB)
        print("Connected to the database.")
        return conn
    except Exception as e:
        print("Error: ", e)
        return None
    

def get_cursor(conn):
    '''
    This function returns the cursor object to the database.
    input: conn (object): Connection object to the database.
    output: cursor (object): Cursor object to the database.'''
    try:
        cursor = conn.cursor()
    except Exception as e:
        print("Error: ", e)
        return None
    return cursor

def get_colums_names(cursor, table_name):
    '''
    This function returns the column names of a table.
    input: cursor (object): Cursor object to the database.
           table_name (str): Name of the table.
    output: columns (list): List of the column names.'''
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [column[0] for column in cursor.description]
    except Exception as e:
        print("Error: ", e)
        return None
    return columns