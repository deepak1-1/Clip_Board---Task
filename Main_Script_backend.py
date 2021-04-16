# ~ user need to run this script every time when he/she switch on his/her laptop using pythonw command
#   instead of python in command prompt
# ~ to store every copied text to Database and delete record saved before 7 days in database


# import section

from Database_Connection import *
from datetime import datetime,timedelta
import pyperclip as pyc




class Scripts( Database ):

    # to run script at backend which will paste copied data to database
    def pasting_backend(self):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)

        today_date = datetime.now().strftime("%d/%m")

        insert_query = "INSERT INTO Clip_data( Data, Date_, Time_) VALUES (?,?,?)"

        previous_text = ""
        flag = 0
        while True:
            if flag == 0:
                copied_text = str(pyc.paste())
                flag = 1
            else:
                copied_text = str(pyc.waitForNewPaste())
            copied_text = copied_text.replace("\r", "").strip()
            if copied_text != previous_text and copied_text != "":
                time_now = datetime.now().strftime("%H:%M")
                previous_text = copied_text

                cursor.execute(insert_query, (copied_text, today_date, time_now))
        

    # to clear clip_data everyday(to delete data which is stored before 7 days)
    def delete_data_before_7_days(self):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)
        
        date_before_7_days = ( datetime.now() - timedelta(days=7) ).strftime("%d/%m")

        delete_query = "DELETE FROM Clip_data where Date_ = (?);"

        cursor.execute(delete_query,(date_before_7_days,))

    # to clear recycle bin daily(to delete data which is stored before 5 days )
    def delete_data_recyclebin_before_5_days(self):
        
        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)
        
        date_before_5_days = ( datetime.now() - timedelta(days=5) ).strftime("%d/%m")

        delete_query = "DELETE FROM Recycle_bin where Date_ = (?);"

        cursor.execute(delete_query,(date_before_5_days,))


if __name__ == "__main__":

    script = Scripts() 

    #to execute delete_data_recyclebin_before_5_days method once in a day
    script.delete_data_recyclebin_before_5_days()

    #to execute delete_data_before_7_days method once in a day
    script.delete_data_before_7_days()

    #to store copied text to database
    script.pasting_backend()
    
