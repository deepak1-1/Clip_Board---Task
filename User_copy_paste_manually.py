#To operate with manually copy paste to our database through clipboard used inside laptop


# Importing Part 
from Database_Connection import *
from tkinter import *
import tkinter.messagebox as tmsg




#to work with reading and writing to database
# inheriting from Database_Connection.Database Class
class DataBase_functions(Database):

    def saving_manual_copy(self,text):
        print(text,type(text))
        

#to provide a interactive GUI using tkinter
class GUI_part(DataBase_functions):#inherited Database functions class

    def manual_copy(self):
        global root
        #closing previous window
        root.destroy()

        root = Tk()
        root.title("Manual Copy")

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
            command = lambda : DataBase_functions.saving_manual_copy(self,text.get("1.0","end")),
            width=15,height=2, relief=GROOVE, border=10,font="lucida 15 bold",
            justify=CENTER, bg="blue",fg="white"
            ).pack(pady=10)
        

        f2.pack(fill=BOTH)#packing frame 2 to cover both space x and y


    
    #To create a gui window to interact with user 
    #asking for manual copy or simply paste to database
    def main_window(self,flag):
        global root
        #so that we can't have error of closing window when we call it first time
        if flag == 0:
            root.destroy()

        root = Tk()
        root.title("Clip Board")

        #Frame to show label what this window is about
        f1 = Frame(root, bg="grey", pady = 20)
        Label(root,text="CLIP BOARD",
              font='lucida 35 bold',
              justify='center').pack()
        f1.pack(fill=X)

        #Frame 2 which have several buttons to perform specified task 
        f2 = Frame(root, pady = 20)

        #on click call manual copy function inside this class
        Button(f2, text="Manual Copy", command=self.manual_copy, font="lucida 25 bold", relief=GROOVE, border=10,
                    justify=CENTER, width=16, height=1).pack()
        

        Button(f2, text="Save To Database", command="text", font="lucida 25 bold", relief=GROOVE, 
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


