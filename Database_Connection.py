#to make a connection to the database and to generate a database if not exists
import sqlite3 as sql

#to return a connector and cursor object of the connected database 
# and do some operations over database table
class Database:

    #constructor
    def __init__(self):
        self.connector = sql.connect("Testing.db")
        self.cur = self.connector.cursor()

    # to create table if not exists
    def create_table(self):
        #Query to create A Table inside Database
        query = """   CREATE TABLE Clip_data(
                            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            Data Char NOT NUll
                        );
                 """
        #handling Exception if table already exists
        try:
            self.cur.execute(query)
            self.connector.commit()
        except Exception as e:
            return e
        else:
            return True

    #to delete main table
    def delete_table(self):
        query = "DROP TABLE Clip_data;"

        self.cur.execute(query)
        self.connector.commit()

    #to return connector object
    def return_connector(self):
        return self.connector


    def return_cursor(self):
        return self.cur



