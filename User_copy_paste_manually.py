#To operate with manually copy paste to our database through clipboard used inside laptop


# Importing Part 
from Database_Connection import *
from tkinter import *
import tkinter.messagebox as tmsg
import pyperclip as pyc



#to work with reading and writing to database
# inheriting from Database_Connection.Database Class
class DataBase_functions(Database):

    def storing_copied_text(self,text):
        cur = Database.return_cursor(self)
        conn = Database.return_connector(self)

        #creating table if not created
        test = Database.create_table(self)

        fetch_query = """
                          SELECT Data from Clip_data order by Id desc LIMIT 1;
                      """

        cur.execute(fetch_query)
        fetched_data = cur.fetchone()

        #part of code will check for repetition of data in and show msg accordingly 
        #if not exists in data it will store it else show msg
        if fetched_data == None or fetched_data[0] != text:
            insert_query = "INSERT INTO Clip_data(Data) VALUES (?);"

            try:
                cur.execute(insert_query,(text,))
                conn.commit()
            except Exception as e:
                tmsg.showinfo("Issue", "There is some in storing({})".format(e))
            else:
                tmsg.showinfo("Successful", "Done!")
        else:
            tmsg.showinfo("Already", "The text you want to store is already stored in Database.")


    #to delete table and re-create it 
    def delete_all(self):

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
class GUI_part(DataBase_functions):#inherited Database functions class

    #method to go back to main window
    def go_back_main_exit(self):
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
        f1 = Frame(root, bg="grey")
        Label(f1,text="Paste your copied part below",
                    font='lucida 25 bold',
                    justify='center',bg="grey").pack()
        f1.pack(fill=X)

        #Frame 2 to paste user copied part and save it using button
        f2 = Frame(root,pady = 20)        
        
        text = Text(f2)
        text.pack(fill=BOTH)

        #to pass text to our database class function when clicked on this button
        Button(f2,text="Save",
            command = lambda : DataBase_functions.storing_copied_text(self,text.get("1.0","end")),
            width=15,height=2, relief=GROOVE, border=10,font="lucida 15 bold",
            justify=CENTER, bg="blue",fg="white"
            ).pack(pady=10)
        

        f2.pack(fill=BOTH)#packing frame 2 to cover both space x and y


    #method will fetch last copied text to screen and ask whether you want to save or not
    #meanwhile you can edit it too
    def checking_last_copied(self):
        global root

        root.destroy()

        root = Tk()
        root.title("Copied Text")

        self.go_back_main_exit()

        f1 = Frame(root, bg="grey")
        Label(f1,text="Previously copied text was shown below,you can edit it too",
                    font='lucida 25 bold',
                    justify='center',bg="grey").pack()
        f1.pack(fill=X)

        f2 = Frame(root)

        text = Text(f2)
        text.pack(fill=BOTH)

        copied_text = str(pyc.paste())
        text.insert("1.0",copied_text)

        #to pass text to our database class function when clicked on this button
        Button(f2,text="Save",
            command = lambda : DataBase_functions.storing_copied_text(self,text.get("1.0","end")),
            width=15,height=2, relief=GROOVE, border=10,font="lucida 15 bold",
            justify=CENTER, bg="blue",fg="white"
            ).pack(pady=10)

        f2.pack(fill=BOTH)


    
    #To create a gui window to interact with user 
    #asking for manual copy or simply paste to database
    def main_window(self,flag):
        global root
        #so that we can't have error of closing window when we call it first time
        if flag == 0:
            root.destroy()

        root = Tk()
        root.title("Clip Board")
        root.minsize(400,450)
        root.maxsize(400,450)

        #Frame to show label what this window is about
        f1 = Frame(root, bg="grey", pady = 20)
        Label(root,text="CLIP BOARD",
              font='lucida 35 bold',
              justify='center').pack()
        f1.pack(fill=X)

        #Frame 2 which have several buttons to perform specified task 
        f2 = Frame(root, pady = 20)

        #on click call manual copy function inside this class
        Button(f2, text="Manual Paste", command=self.manual_paste, font="lucida 25 bold",
                     relief=GROOVE, border=10,
                    justify=CENTER, width=16, height=1).pack()
        

        Button(f2, text="Save(Last copied)", command=self.checking_last_copied,
                     font="lucida 25 bold", relief=GROOVE, 
                    border=10, justify=CENTER, width=16, height=1).pack()

        Button(f2, text="Delete All Record", command=lambda : DataBase_functions.delete_all(self),
                    font="lucida 25 bold", relief=GROOVE, 
                    border=10, justify=CENTER, width=16, height=1).pack()
        
        #on click will quit the GUI window 
        Button(f2, text="Exit", command=quit, font="lucida 25 bold", relief=GROOVE, border=10,
                    justify=CENTER, bg="RED", fg="white", width=8, height=1).pack()
        

        f2.pack(fill=X) #packing frame 2

if __name__ == "__main__":
    gui = GUI_part()
    gui.main_window(1)
    root.mainloop()
    # Database.return_connector(1).close()


