

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

    def delete_(self, index_, dict_of_elements, edited_text, text_widget):

        cursor = Database.return_cursor(self)
        connector = Database.return_connector(self)

        edited_text = edited_text.strip()
        
        if edited_text == dict_of_elements[index_] :

            delete_clip_data_query = "DELETE FROM Clip_data WHERE Id = (?);"
            insert_recycle_bin_query = """
                                        INSERT INTO Recycle_bin(Data) VALUES (?);
                                       """

            try:
                cursor.execute(delete_clip_data_query, (index_, ))
                cursor.execute(insert_recycle_bin_query, (edited_text, ))
                connector.commit()
                text_widget.delete("1.0","end")
                dict_of_elements.pop(index_)
            except Exception as e:
                tmsg.showinfo("Issue", "Some Issue\n\r{}".format(e))
            else:
                tmsg.showinfo("Deleted","Successfully Done!")
                self.copied_element_showing( dict_of_elements )
        else:
            tmsg.showinfo("Issue","you have edited text if you want to delete don't edit")


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

class In_out_recycle_bin_data( Database ):

    pass


if __name__ == "__main__":

    test = In_out_clip_data() 
    test.fetch_previous_n_saved(5)

