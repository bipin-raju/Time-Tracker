import sqlite3
from sqlite3 import Error

class DataBaseAdapter:    
    def __init__(self):        
        self.connection = self.create_connection("Data/log.db")


    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection


    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            # print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")


    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    ## SQL commands ###
    create_todays_table = """
    CREATE TABLE IF NOT EXISTS '{}' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT NOT NULL,
    category INTEGER,
    task_name TEXT,
    start_time REAL,
    end_time REAL,
    total_time INTEGER
    );
    """

    insert_activity = """
    INSERT INTO
    '{}' (app_name, category, task_name, start_time, end_time, total_time)
    VALUES
    ('{}', {}, '{}', julianday('{}'), julianday('{}'), {});
    """

    get_all_activities_from_today = "SELECT * from {}"
