#to make a connection to the database and to generate a database if not exists
import sqlite3 as sql

#to return a connector and cursor object of the connected database 
# and do some operations over database table
class Database:

    #constructor to make connections with database and create recycle bin table
    def __init__(self):
        self.connector = sql.connect("Testing.db")
        self.cur = self.connector.cursor()

        
    def create_table_recycle_bin(self):

        recycle_bin_query = """ CREATE TABLE Recycle_bin(
                                 Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                 Data CHAR NOT NUll,
                                 Date_ CHAR NOT NULL   
                                );
                            """

        try:
            self.cur.execute(recycle_bin_query)
            self.connector.commit()
        except Exception as e:
            return e
        else:
            return True

    # to create table if not exists
    def create_table_clip_data(self):
        #Query to create A Table inside Database
        query = """   CREATE TABLE Clip_data(
                            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            Data CHAR NOT NUll,
                            Date_ CHAR NOT NULL,
                            Time_ CHAR NOT NULL
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

    #to delete table's data specified by user 
    def delete_data_inside_table(self, table_name):

        delete_query = "DELETE FROM {};".format( table_name )

        try:

            self.cur.execute(delete_query)
            self.connector.commit()
        except Exception as e:
            return e
        else:
            return True

    #to return connector object
    def return_connector(self):
        return self.connector

    #to return cursor object
    def return_cursor(self):
        return self.cur



if __name__ == "__main__":

    db = Database()

    db.create_table_clip_data()
    db.create_table_recycle_bin()
    