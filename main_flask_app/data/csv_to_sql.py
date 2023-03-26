import sqlite3
import pandas as pd
import os

def creating_dataset_tables():
    basedir = os.path.abspath(os.path.dirname(__file__))

    # ---------------------------------------------
    # Define and create the database using sqlite3
    # ---------------------------------------------

    # Define the database file name and location
    db_file = (basedir + "/cycle_parking.db")

    # Connect to the database
    connection = sqlite3.connect(db_file)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    drop_old_cycle_parking_table = """DROP TABLE IF EXISTS cycle_parking_data;"""
    drop_old_boroughs_list_table = """DROP TABLE IF EXISTS boroughs_list;"""

    # Dataset tables definition in SQL
    create_cycle_parking_table = """CREATE TABLE IF NOT EXISTS cycle_parking_data(
                    feature_id TEXT PRIMARY KEY,
                    prk_cover TEXT NOT NULL,
                    prk_secure TEXT NOT NULL,
                    prk_locker TEXT NOT NULL,
                    prk_cpt FLOAT NOT NULL,
                    borough TEXT NOT NULL,
                    photo1_url TEXT NOT NULL,
                    photo2_url TEXT NOT NULL,
                    latitude FLOAT NOT NULL,
                    longitude FLOAT NOT NULL);
                    """

    create_boroughs_list_table = """CREATE TABLE IF NOT EXISTS boroughs_list(
                    borough TEXT PRIMARY KEY);
                    """

    cursor.execute(drop_old_cycle_parking_table)
    connection.commit()
    cursor.execute(drop_old_boroughs_list_table)
    connection.commit()

    cursor.execute(create_cycle_parking_table)
    connection.commit()
    cursor.execute(create_boroughs_list_table)
    connection.commit()

    cycle_parking_info = (basedir + "/cycle_parking_data.csv")
    cycle_parking_df = pd.read_csv(cycle_parking_info, keep_default_na=False)
    cycle_parking_df.to_sql("cycle_parking_data", connection,
                    if_exists="append",
                    index=False,)

    boroughs_list = (basedir + "/boroughs_list.csv")
    boroughs_list_df = pd.read_csv(boroughs_list, keep_default_na=False)
    boroughs_list_df.to_sql("boroughs_list", connection,
                    if_exists="append",
                    index=False,)

    connection.close()

if __name__ == '__main__':
    creating_dataset_tables()