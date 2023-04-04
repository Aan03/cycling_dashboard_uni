import sqlite3
import pandas as pd
import os
from passlib.hash import sha256_crypt

def selenium_db_setup():
    username = "existing_test_user"
    password = "test_raw_password"
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_file = (basedir + "/test_selenium.db")
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    drop_users_table = """DROP TABLE IF EXISTS users;"""
    drop_reports_table = """DROP TABLE IF EXISTS reports;"""
    cursor.execute(drop_users_table)
    connection.commit()
    cursor.execute(drop_reports_table)
    connection.commit()
    create_users_table = """CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL);
                    """
    create_reports_table = """CREATE TABLE IF NOT EXISTS reports(
                    id INTEGER PRIMARY KEY,
                    reporter_id INTEGER NOT NULL,
                    rack_id TEXT NOT NULL,
                    report_date DATETIME NOT NULL,
                    report_borough TEXT NOT NULL,
                    report_time DATETIME NOT NULL,
                    report_details TEXT NOT NULL
                    );
                    """
    
    cursor.execute(create_users_table)
    connection.commit()

    cursor.execute(create_reports_table)
    connection.commit()
    encrypted_password = sha256_crypt.hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES(?, ?)", 
                   (username, encrypted_password))
    connection.commit()
    cursor.execute('''INSERT INTO reports (reporter_id, rack_id, report_date, 
                    report_borough, report_time, report_details) VALUES(?, ?, ?, ?, ?, ?)''', 
                   (1, "RWG004615", "2023-04-02", "Islington", "12:45", "test report"))
    connection.commit()

if __name__ == '__main__':
    selenium_db_setup()