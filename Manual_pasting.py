#To operate with manually copy paste to our database through clipboard used inside laptop


# Importing Part 
from Database_Connection import *
from tkinter import *
from datetime import datetime
import tkinter.messagebox as tmsg
import pyperclip as pyc



#to work with reading and writing to database
# inheriting from Database_Connection.Database Class
class DataBase_functions(Database):

    #to save copied thing to our database it will through messagebox depending whether successful or not 
    def storing_copied_text( self, text ):

        # whenever text widget is empty it will return a empty text so to handle that we checked it 
        if text != "\n":

            # connecting to database and using it's function through parent class Database
            #cur to execute sql query and conn to commit the changes same time
            cur = Database.return_cursor(self)
            conn = Database.return_connector(self)

            #creating table if not created
            Database.create_table(self)

            # to fetch details of previously saved copied thing
            fetch_query = """
                              SELECT Data from Clip_data order by Id desc LIMIT 1;
                          """
            cur.execute(fetch_query)

            #to store Fetched data, fetched during execution of above fetch_query
            fetched_data = cur.fetchone()

            #part of code will check for repetition of data in and show message accordingly 
            #if not exists in lastly added data it will store it else show message
            #It checks too for first time storing to database 
            if fetched_data == None or fetched_data[0] != text:

                #taking date and time for that instance and storing it too
                datetime_now = datetime.now()#created datetime object

                #used datetime.datetime.strftime(format) function to get specified format and 
                #split them using string function split on the basis of space between them 
                today_date,time_now = (datetime_now.strftime("%d/%m/%Y %H:%M")).split()

                # generated insert query which on execution will store details in Database
                insert_query = "INSERT INTO Clip_data( Data, Date_, Time_) VALUES (?,?,?);"

                #try except block to handle Exceptions raised during execution of query
                try:
                    cur.execute(insert_query, ( text, today_date, time_now, ))
                    conn.commit()
                except Exception as e:
                    tmsg.showinfo("Issue", "There is some issue in storing \n{}".format(e))
                else:#try - else ends here
                    tmsg.showinfo("Successful", "Done!")

            else:#fetched data checking -else ends here
                tmsg.showinfo("Already", "The text you want to store is already stored in Database.")

        else:#else of - text argument provided in method call ends here
            tmsg.showinfo("Error","Please don't make empty entry!")


    #to delete table and re-create it 
    def delete_all(self):

        # tkinter.messagebox.askquestion() return yes or no so to store we created answer variable
        answer = tmsg.askquestion("Sure?","Do you want to delete all record saved Previously?")

        if answer == "yes":
            Database.delete_table(self)

            return_stat = Database.create_table(self)

            if return_stat:
                tmsg.showinfo("Successful", "Done!")
            else:
                tmsg.showinfo("Issue","Some issue({})".format(return_stat))
        else:
            tmsg.showinfo("Stopped", "Successfully Terminated!")
        
        

#to provide a interactive GUI using tkinter
class GUI_part(DataBase_functions):#inherited From Manual_pasting.Database_functions class


    #method to go back to main window and quiting the app
    def go_back_main_exit(self):

        # created menu in root as root is global everywhere, so there is no error
        Menubar = Menu(root)
        Menubar.add_command(label='Go back',command=lambda : self.main_window(0))
        Menubar.add_command(label="Exit",command=quit)
        root.config(menu=Menubar)


    #allow user to manually paste their copied text to save it in database
    def manual_paste(self):
        global root
        #closing previous window
        root.destroy()

        root = Tk()
        root.title("Manual Copy")

        self.go_back_main_exit()

        #Frame to help user what to do
        heading = Frame(root, bg="grey")
        Label(heading,text="Paste your copied part below",
                    font='lucida 25 bold',
                    justify='center',bg="grey").pack()
        heading.pack(fill=X)        

        #Frame 2 to paste user copied part and save it using button
        text_frame = Frame(root,pady = 20)

        #adding scrollbar to text_frame to make ease of going up and down in long copied text
        scroll_bar = Scrollbar(text_frame) #vertical scrollbar  
        scroll_bar.pack(side = RIGHT, fill = Y)       
        
        #to paste copied text by user
        text = Text(text_frame, yscrollcommand = scroll_bar.set)
        text.pack(fill=BOTH)

        scroll_bar.config( command = text.yview )#adding it to text widget

        #to pass text to our database class function when clicked on this button
        Button(text_frame,text="Save",
            command = lambda : DataBase_functions.storing_copied_text(self,text.get("1.0","end")),
            width=15,height=2, relief=GROOVE, border=10,font="lucida 15 bold",
            justify=CENTER, bg="blue",fg="white"
            ).pack(pady=10)
        

        text_frame.pack(fill=BOTH)#packing frame 2 to cover both space x and y



    #method will fetch last copied text to screen and ask whether you want to save or not
    #meanwhile you can edit it too
    def checking_last_copied(self):
        global root

        root.destroy()

        root = Tk()#creating window
        root.title("Copied Text")

        self.go_back_main_exit()#calling method GUI_part.go_back_main_exit(self)

        heading = Frame(root, bg="grey")#heading Frame 
        Label(heading,text="Previously copied text is shown below,you can edit it too",
                    font='lucida 25 bold',
                    justify='center',bg="grey").pack()
        heading.pack(fill=X)

        text_frame = Frame(root)#Frame - to take text from clipboard  

        #adding scrollbar to text_frame to make ease of going up and down in long copied text
        scroll_bar = Scrollbar(text_frame)  
        scroll_bar.pack(side = RIGHT, fill = Y)       
        
        #to paste copied text by user
        text = Text(text_frame, yscrollcommand = scroll_bar.set)
        text.pack(fill=BOTH)

        scroll_bar.config( command = text.yview )#adding it to text widget

        copied_text = str(pyc.paste())
        text.insert("1.0",copied_text)

        #to pass text to our database class function when clicked on this button
        Button(text_frame,text="Save",
            command = lambda : DataBase_functions.storing_copied_text(self,text.get("1.0","end")),
            width=15,height=2, relief=GROOVE, border=10,font="lucida 15 bold",
            justify=CENTER, bg="blue",fg="white"
            ).pack(pady=10)

        text_frame.pack(fill=BOTH)


    
    #To create a gui window to interact with user 
    #asking for manual copy or simply paste to database
    def main_window(self,flag):

        global root

        #flag = 1 - when It is called using object of class else 0  
        #so that we can't have error of closing window when we call it first time
        if flag == 0:
            root.destroy()

        root = Tk()#creating GUI window
        root.title("Clip Board")
        #fixing it's size
        root.minsize(400,450)
        root.maxsize(400,450)

        #Frame to show label what this window is about
        heading = Frame(root, bg="grey", pady = 20)
        Label(root,text="CLIP BOARD",
              font='lucida 35 bold',
              justify='center').pack()
        heading.pack(fill=X)

        #Frame 2 which have several buttons to perform specified task 
        text_frame = Frame(root, pady = 20)

        #on click call manual copy function inside this class
        Button(text_frame, text="Manual Paste", command=self.manual_paste, font="lucida 25 bold",
                     relief=GROOVE, border=10,
                    justify=CENTER, width=16, height=1).pack()
        

        Button(text_frame, text="Save(Last copied)", command=self.checking_last_copied,
                     font="lucida 25 bold", relief=GROOVE, 
                    border=10, justify=CENTER, width=16, height=1).pack()

        Button(text_frame, text="Delete All Record", command=lambda : DataBase_functions.delete_all(self),
                    font="lucida 25 bold", relief=GROOVE, 
                    border=10, justify=CENTER, width=16, height=1).pack()
        
        #on click will quit the GUI window 
        Button(text_frame, text="Exit", command=quit, font="lucida 25 bold", relief=GROOVE, border=10,
                    justify=CENTER, bg="RED", fg="white", width=8, height=1).pack()
        

        text_frame.pack(fill=X) #packing frame 2


if __name__ == "__main__":
    gui = GUI_part()
    gui.main_window(1)
    root.mainloop()
    


