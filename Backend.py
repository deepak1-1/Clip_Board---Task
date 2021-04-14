

# Importing Part 
from Database_Connection import * 
from tkinter import *
import tkinter.messagebox as tmsg
import pyperclip as pyc



class In_out_clip_data( Database ):

    
    # To fetched previously saved last n entry which user want to fetch  
    def fetch_previous_n_saved(self, n_previous ):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)

        fetch_query = "SELECT Id,Data FROM Clip_data ORDER BY Id Desc limit {}".format( n_previous )

        cursor.execute( fetch_query )
        fetch_data = cursor.fetchall()

        if len(fetch_data) != n_previous:
            tmsg.showwarning("Error","""There are not much data inside database you want to fetch
                                     \rmaximum last data you can fetch for now is {}
                                  """.format(len(fetch_data)))
            return False
        else:
            return dict(fetch_data)

    def copy_(self, index_, dict_of_elements, edited_text):

        previously_copied_text = pyc.paste()

        previously_copied_text = previously_copied_text.replace("\r","").strip()
        
        edited_text = edited_text.strip()

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

    def delete_(self, index_, dict_of_elements, edited_text):
        print(edited_text)
        pass

    def update_(self, index_, dict_of_elements, edited_text):
        print(edited_text)
        pass


class In_out_recycle_bin_data( Database ):

    pass


if __name__ == "__main__":

    test = In_out_clip_data() 
    test.fetch_previous_n_saved(5)

