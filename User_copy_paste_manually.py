#To operate with manually copy paste to our database through clipboard used inside laptop


# Importing Part 
from Database_Connection import *
from tkinter import *



#to work with reading and writing to database
class DataBase_functions(Database):

    def __init__(self):
        self.cur = Database.return_cursor(self)
        self.conn = Database.return_connector(self)
        

#to provide a interactive GUI using tkinter
class GUI_part(DataBase_functions):#inherited Database functions class
    
    pass
   


if __name__ == "__main__":
    pass


