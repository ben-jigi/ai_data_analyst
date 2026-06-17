import sqlite3
import pandas as pd


def sql_database(df):

    conn= sqlite3.connect(
        "database.db"
    )

    df.to_sql(
        "data",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

def run_query(sql_query):


    conn = sqlite3.connect(
        "database.db"
    )

    result = pd.read_sql_query(
        sql_query,
        conn
    )

    conn.close()

    return result