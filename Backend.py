

# Importing Part 
from Database_Connection import * 
from tkinter import *
from datetime import datetime,timedelta
import tkinter.messagebox as tmsg
import pyperclip as pyc


#it will provide function for database used to manipulate main clip_data
class In_out_clip_data( Database ):

    #to return particular date's data of which user want to look
    def fetch_for_particular_date(self, date_):# date format dd/mm/yyyy

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)

        today_date = datetime.now().date()
        date_before_6_days = ( today_date - timedelta( days=6 ))
        
        try:
            user_date = datetime.strptime( date_, "%d/%m/%Y").date()
        except ValueError:
            tmsg.showinfo("Not Valid","Date you entered either not in given format or invalid")
            return
        else:
            "Done"

        if user_date > today_date:
            tmsg.showinfo("Future Date","You selected future Date, select again")
        elif user_date < date_before_6_days :
            tmsg.showinfo("Issue","we can only have last six days data,choose date accordingly")
        else:
            date_to_fetch = user_date.strftime("%d/%m")
            fetch_query = "SELECT Id,Data FROM Clip_data where Date_ = (?);"

            cursor.execute(fetch_query, (date_to_fetch,))
            fetched_data = cursor.fetchall()

            self.copied_element_showing( dict(fetched_data) )


    
    # To fetched previously saved last n entry which user want to fetch  
    def fetch_previous_n_saved(self, n_previous ):

        if n_previous != 0:

            cursor = Database.return_cursor(self)
            connector = Database.return_connector(self)

            fetch_query = "SELECT Id,Data FROM Clip_data ORDER BY Id Desc limit {}".format( n_previous )

            cursor.execute( fetch_query )
            fetch_data = cursor.fetchall()

            if len(fetch_data) != n_previous:
                tmsg.showwarning("Error","""There are not much data inside database you want to fetch
                                         \rmaximum last data you can fetch for now is {}
                                      """.format(len(fetch_data)))
            else:
                self.copied_element_showing( dict(fetch_data) )
        else:
            tmsg.showinfo("Empty","Enter number!")

    def copy_(self, index_, dict_of_elements, edited_text):

        previously_copied_text = pyc.paste()#to get last copied text
        previously_copied_text = previously_copied_text.replace("\r","").strip()        
        edited_text = edited_text.strip()

        #checking for last copied text whether it is same or what
        #also checking is user edited text shown in text widget or not then asking it some questions
        if dict_of_elements[index_] == edited_text:
            if edited_text != previously_copied_text:
                pyc.copy( edited_text )
                tmsg.showinfo("","Done!")
            else:
                tmsg.showinfo("Already!","Text you want to copy already copied")
        else:
            answer = tmsg.askquestion("Sure?","You edited text you want to copy edited text?")
            if answer == "yes":
                if edited_text != previously_copied_text:
                    pyc.copy( edited_text )
                    tmsg.showinfo("","Done!")
                else:
                    tmsg.showinfo("Already!","Text you want to copy already copied")
            else:
                answer = tmsg.askquestion("?","you want to copy main(not edited) text?")
                if answer == "yes":
                    if dict_of_elements[index_] != previously_copied_text:
                        pyc.copy( edited_text )
                        tmsg.showinfo("","Done!")
                    else:
                        tmsg.showinfo("Already!","Text you want to copy already copied")
                else:
                    tmsg.showwarning( "Not Done", "Not copied any text")

    #to deleted selected element and then show remaining values again
    #if there is no value left after deletion then it will show recycle bin
    def delete_(self, index_, dict_of_elements, edited_text, text_widget):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)
        today_date = datetime.now().strftime("%d/%m")
        edited_text = edited_text.strip()
        
        if edited_text == dict_of_elements[index_] :

            delete_clip_data_query = "DELETE FROM Clip_data WHERE Id = (?);"
            insert_recycle_bin_query = """
                                        INSERT INTO Recycle_bin(Data,Date_) VALUES (?,?);
                                       """

            try:
                cursor.execute(delete_clip_data_query, (index_, ))
                cursor.execute(insert_recycle_bin_query, (edited_text, today_date, ))
                connector.commit()
                text_widget.delete("1.0","end")
                dict_of_elements.pop(index_)
            except Exception as e:
                tmsg.showinfo("Issue", "Some Issue\n\r{}".format(e))
            else:
                tmsg.showinfo("Deleted","Moved to recycle bin")
                if dict_of_elements :
                    self.copied_element_showing( dict_of_elements )
                else:
                    self.fetch_all_data_recycle_bin()
        else:
            tmsg.showinfo("Issue","you have edited text if you want to delete don't edit")


    #to update a text which user want to edit if not edited then showing messages
    def update_(self, index_, dict_of_elements, edited_text, text_widget):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)
        edited_text = edited_text.strip()

        if edited_text != dict_of_elements[index_] :

            update_query = "UPDATE  Clip_data set Data = (?) where Id = (?);"

            try:
                cursor.execute(update_query,( edited_text, index_ ))
                connector.commit()
                dict_of_elements[index_] = edited_text
            except Exception as e:
                tmsg.showinfo("Issue","Some Issue\n\r{}".format(e))
            else:
                tmsg.showinfo("Done","Successfully Updated")
                self.copied_element_showing( dict_of_elements )

        else:
            tmsg.showinfo("Issue","You haven't edited main text, can't update")


    #it will move all text to recycle bin and then show recycle bin 
    def delete_all(self, dict_of_elements):

        answer = tmsg.askquestion("Sure?","Are you sure you want to delete all?")
        if answer == "yes":

            today_date = datetime.now().strftime("%d/%m")
            cursor = Database.return_cursor(self)
            connector = Database.return_connector(self)        
            delete_query = "DELETE FROM Clip_data WHERE Id = (?);"
            recycle_query = "INSERT INTO Recycle_bin( Data, Date_) VALUES (?,?);"

            try:
                for key in dict_of_elements:
                    cursor.execute(delete_query,(key,))
                    cursor.execute(recycle_query,(dict_of_elements[key], today_date,))
                connector.commit()
                dict_of_elements.clear()
            except Exception as e:
                tmsg.showinfo("Issue","Issue - {}".format(e))
            else:
                tmsg.showinfo("Deleted","Moved to recycle bin")
                self.fetch_all_data_recycle_bin(  )
        else:
            tmsg.showinfo("stopped","Not deleted any text")



#class to provide functionality to recycle bin data
class In_out_recycle_bin_data( Database ):

    #to show all data inside recycle bin
    def fetch_all_data_recycle_bin(self):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)
        fetch_query = "SELECT Id,Data From Recycle_bin;"

        cursor.execute(fetch_query)
        fetched_data = cursor.fetchall()

        self.recycle_bin_data_showing( dict(fetched_data) )

    #to show data for particular date
    def fetch_data_for_date(self, user_date):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)
        today_date = datetime.now().date()
        date_before_4_days = ( today_date - timedelta( days=4 ))
        
        try:
            user_date = datetime.strptime( user_date, "%d/%m/%Y").date()
        except ValueError:
            tmsg.showinfo("Not Valid","Date you entered either not in given format or invalid")
            return
        else:
            "Done"

        if user_date > today_date:
            tmsg.showinfo("Invalid","Future date!")
        elif user_date < date_before_4_days :
            tmsg.showinfo("No record","Don't provide date before than 4 days")
        else:
            date_to_fetch = user_date.strftime("%d/%m")
            fetch_query = "SELECT Id,Data FROM Recycle_bin where Date_ = (?);"

            cursor.execute(fetch_query, (date_to_fetch,))
            fetched_data = cursor.fetchall()

            self.recycle_bin_data_showing( dict(fetched_data) )

    #to store data again to main clip_data table
    def restore_(self, index_, dict_of_elements):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)
        today_date,time_now = datetime.now().strftime("%d/%m %H:%M").split()

        delete_query = "DELETE FROM Recycle_bin WHERE Id = (?);"
        restore_query = "INSERT INTO Clip_data(Data, Date_, Time_) VALUES (?,?,?);" 
        
        #handling exception if any during inserting data inside database or removing it from
        try:
            cursor.execute(delete_query,(index_,))
            cursor.execute(restore_query,(dict_of_elements[index_], today_date, time_now,))
            connector.commit()
            dict_of_elements.pop( index_ )
        except Exception as e:
            tmsg.showinfo("Issue","Issue - {}".format(e))
        else:
            tmsg.showinfo("Restored","Restored Successfully")
            if dict_of_elements:
                self.recycle_bin_data_showing( dict_of_elements )
            else:
                self.main_window( 0 )

    #to delete selected recycle bin data through user 
    def delete_(self, index_, dict_of_elements):


        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)        
        delete_query = "DELETE FROM Recycle_bin WHERE Id = (?);"

        #handling error if any
        try:
            cursor.execute(delete_query, (index_,))
            connector.commit()
            dict_of_elements.pop( index_ )
        except Exception as e:
            tmsg.showinfo("Issue","Issue - {}".format(e))
        else:
            tmsg.showinfo("Deleted","Permanently deleted text!")

            if dict_of_elements:
                self.recycle_bin_data_showing( dict_of_elements )
            else:
                self.main_window( 0 )

    #to restore all data which is inside dic_of_elemnts provided by user
    # and will redirect you to main window after success
    def restore_all(self, dict_of_elements):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)        
        today_date = datetime.now().strftime("%d/%m")
        delete_query = "DELETE FROM Recycle_bin WHERE Id = (?);"
        store_query = "INSERT INTO Clip_data(Data,Date_,Time_) VALUES (?,?,?);"

        try:
            for key in dict_of_elements:
                time_now = datetime.now().strftime("%H:%M")
                cursor.execute(delete_query,(key,))
                cursor.execute(store_query,(dict_of_elements[key],today_date,time_now))
            connector.commit()
            dict_of_elements.clear()
        except Exception as e:
            tmsg.showinfo("Issue","Issue - {}".format(e))
        else:
            tmsg.showinfo("Restored","Successfully restored all")

            self.main_window(0)


    #to delete all data inside dict_of_elements permanently 
    # and redirect you to main window again
    def delete_all(self, dict_of_elements):

        answer = tmsg.askquestion("Sure","Are you sure you want to delete all data Permanently?")

        if answer == "yes":
            cursor = Database.return_cursor(self)
            connector = Database.return_connector(self)        
            delete_query = "DELETE FROM Recycle_bin WHERE Id = (?);"

            try:
                for key in dict_of_elements:
                    cursor.execute(delete_query,(key,))
                connector.commit()
                dict_of_elements.clear()
            except Exception as e:
                tmsg.showinfo("Issue","Issue - {}".format(e))
            else:
                tmsg.showinfo("Deleted","Permanently Deleted All")
                self.main_window(0)
        else:
            tmsg.showinfo("Stopped","Not deleted any stored text in recycle bin")

if __name__ == "__main__":

    """
     you can use the above classes here
     just create object of class and use it's methods 
    """

