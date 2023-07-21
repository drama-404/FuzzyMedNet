"""
db_connection.py

This module provides functions for establishing a connection to a PostgreSQL database.

Author: Denada Rama
Date: 16/06/2023

"""
import psycopg2
import getpass
import pandas as pd

user = 'postgres'
host = 'localhost'


def create_connection(dbname='mimic'):
    """
    Creates a connection to the PostgreSQL MIMIC-III database.
    """
    # Prompt the user to enter the password for the database
    password = getpass.getpass(prompt='Password:')

    # Create a connection to the PostgreSQL database
    con = psycopg2.connect(
        dbname=dbname,
        user=user,
        host=host,
        password=password
    )

    # Create a cursor object for executing queries
    cur = con.cursor()
    return con


def query_data(query, con):
    """
    Executes an SQL query on a database connection and returns the results as a DataFrame.
    """
    # Execute the SQL query and retrieve the results as a DataFrame
    result_df = pd.read_sql_query(query, con)
    return result_df


def select_table(table_name, con):
    """
    Executes and SQL SELECT * query on a specified table
    """
    query = "SELECT * FROM {};".format(table_name)
    df = pd.read_sql_query(query, con)
    return df


def query_sql_file(fname, con):
    """
    Executes an SQL file with multiple queries on a database connection and returns the results as a DataFrame
    """
    # Read the SQL queries from the file
    with open(fname, 'r') as file:
        queries = file.read()

    # Split the queries into individual statements
    query_list = queries.split(';')

    # Remove leading/trailing whitespace from each query
    query_list = [query.strip() for query in query_list]

    return query_list




