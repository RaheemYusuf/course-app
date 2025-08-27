"""
This module handles interactions with a DuckDB database,
including creating tables, inserting data, and querying data.

It uses configuration settings defined in the config module to determine
the database path and data file name.
"""

import duckdb

from config import db_settings


# create a table and insert data
def create_table_and_insert_data():
    """
    Creates a table in the DuckDB database and inserts data from a CSV file.
    """
    data_path = db_settings.data_file_name
    database_path = db_settings.database_path
    sql_query1 = f"""
    CREATE OR REPLACE TABLE rent_apartments AS
    SELECT *
    FROM read_csv_auto('{data_path}');
    """
    with duckdb.connect(f'{database_path}') as con:
        con.sql(sql_query1)
        print("Table created and data inserted successfully!")  # noqa: WPS421


# Run the function to create the table and insert data
print(create_table_and_insert_data())  # noqa: WPS421


# show the tables in the database
def show_tables():
    """
    Shows the tables present in the DuckDB database.
    """
    database_path = db_settings.database_path
    sql_query = """
    Show tables;
    """
    with duckdb.connect(f'{database_path}') as con:
        print(con.sql(sql_query).df())  # noqa: WPS421


def query_data():
    """
    Queries all data from the rent_apartments table in the DuckDB database.

    Returns:
        df (pandas.DataFrame): DataFrame containing the queried data.
    """
    database_path = db_settings.database_path
    sql_query = """
    SELECT * FROM rent_apartments;
    """
    with duckdb.connect(f'{database_path}') as con:
        df = con.sql(sql_query).df()
    return df
