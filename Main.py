#Provide GUI options to some selected database entry by user 

#import Section
from Backend import *
# from tkinter import *
# import tkinter.messagebox as tmsg
# import pyperclip as pyc


class go_back_menu:

    def go_back_and_exit_menu(self,function_to_go):

        Menubar = Menu(root)
        Menubar.add_command(label='Go back',command=function_to_go)
        Menubar.add_command(label="Exit",command=quit)
        root.config(menu=Menubar)


class GUI_clip( In_out_clip_data, go_back_menu ):

    def copied_element_options( self, index_, dict_of_elements ):

        global root

        if dict_of_elements != {}:

            if index_ in dict_of_elements.keys():
                root.destroy()

                root = Tk()
                root.title("Options")
                root.geometry("1200x600")

                self.go_back_and_exit_menu( 
                                            lambda : self.copied_element_showing(dict_of_elements)  
                                            )

                heading_frame = Frame(root,bg="grey")
                Label(heading_frame,text="You have selected under shown text, you directly can edit if you want", 
                     font='lucida 25 bold', justify='center', bg="grey").pack()
                heading_frame.pack(fill=X)

                main_frame = Frame(root)

                text_frame = Frame(main_frame,pady = 10, padx = 10)
                #adding scrollbar to text_frame to make ease of going up and down in long copied text
                scroll_bar = Scrollbar(text_frame) #vertical scrollbar  
                scroll_bar.pack(side = RIGHT, fill = Y)       
                
                #to paste copied text by user
                text = Text(text_frame, yscrollcommand = scroll_bar.set, height=15, padx=10,width=120)
                text.pack(fill=BOTH)

                text.insert("1.0", "{}".format( dict_of_elements[index_]))
                scroll_bar.config( command = text.yview )

                text_frame.pack(fill = BOTH)

                options_frame = Frame(main_frame,pady=10)

                Button(options_frame, text="Copy", justify=CENTER, 
                       command=lambda : In_out_clip_data.copy_(self, index_, dict_of_elements, 
                                                                text.get("1.0", "end")),
                       fg="white", relief=GROOVE, border=10,
                       bg="blue", height=1, width=10, font="lucida 15 bold").pack()

                Button(options_frame, text="Save", justify=CENTER, 
                       command=lambda : In_out_clip_data.update_(self, index_, dict_of_elements, 
                                                                  text.get("1.0", "end"), text),
                       fg="white", relief=GROOVE, border=10,
                       bg="blue", height=1, width=10, font="lucida 15 bold").pack()
                
                Button(options_frame, text="Delete", justify=CENTER, 
                       command=lambda : In_out_clip_data.delete_(self, index_, dict_of_elements,
                                                                  text.get("1.0", "end"), text),
                       fg="white", relief=GROOVE, border=10,
                       bg="red", height=1, width=10, font="lucida 15 bold").pack()

                options_frame.pack()

                main_frame.pack()

            else:
                tmsg.showwarning("Error","Index you chosen {} is not in Data Display".format(index_))

        else:
            tmsg.showinfo('No Data',"There is no data")


    def copied_element_showing(self, dict_of_elements):
        global root

        if dict_of_elements:
            root.destroy()        

            root = Tk()
            root.title("Data - Clip Board")
            root.geometry("1200x630")

            self.go_back_and_exit_menu(lambda : self.main_window( 0 ))

            heading_frame = Frame(root,bg="grey")
            Label(heading_frame,text="DATA DISPLAY", font='lucida 35 bold', justify='center', bg="grey").pack()
            heading_frame.pack(fill=X)


            main_frame = Frame(root)

            text_frame = Frame(main_frame,pady = 10, padx = 10)
            
            scroll_bar = Scrollbar(text_frame) #vertical scrollbar  
            scroll_bar.pack(side = RIGHT, fill = Y)       
            
            #to paste copied text by user
            text = Text(text_frame, yscrollcommand = scroll_bar.set, height=20)
            text.pack(fill=BOTH)

            for i in dict_of_elements:
                text.insert("1.0", "\n\n{}.\n{}".format(i, dict_of_elements[i]))
                text.insert("1.0", "\n"+"x"*60)

            scroll_bar.config( command = text.yview ) 

            text_frame.pack(fill = BOTH)


            option_frame = Frame(main_frame)

            Label(option_frame,text="Fill Index of text you want to select(given at starting of each text )",
                     font='lucida 20 bold', justify='center').pack()

            index_ = IntVar(option_frame)

            index_entry = Entry(option_frame, textvariable = index_, relief = SUNKEN,font = "lucida 20 bold")
            index_entry.pack()
            
            Button(option_frame,text="Select",command= lambda: self.copied_element_options(index_.get(), 
                                                                                            dict_of_elements),
                    bg="blue", fg="white", justify=CENTER, height=1, width=10, relief=GROOVE,
                    border=10, font = "lucida 15 bold").pack(pady=10)

            Button(option_frame, text="Delete All",
                    command = lambda : In_out_clip_data.delete_all( self, dict_of_elements),
                    bg = "red", fg = "white", height=1, width = 12, relief = GROOVE,
                    border = 10, font = "lucida 15 bold").pack(pady=5, padx=10,side=RIGHT)

            option_frame.pack(side = BOTTOM, fill = BOTH)

            main_frame.pack(fill = BOTH)

        else:
            tmsg.showinfo('No Data',"There is no data")




class GUI_Recycle( In_out_recycle_bin_data, go_back_menu ):

    def options_for_recycle_bin_data(self, index_, dict_of_elements):
        global root

        if dict_of_elements != {}:

            if index_ in dict_of_elements.keys():
                root.destroy()

                root = Tk()
                root.title("Options")
                root.geometry("1200x600")

                self.go_back_and_exit_menu(lambda : self.recycle_bin_data_showing(dict_of_elements))

                heading_frame = Frame(root,bg="grey")
                Label(heading_frame,
                     text="Selected under shown text(don't edit, first shown text will be in function)", 
                     font='lucida 25 bold', justify='center', bg="grey").pack()
                heading_frame.pack(fill=X)

                main_frame = Frame(root)

                text_frame = Frame(main_frame,pady = 10, padx = 10)
                #adding scrollbar to text_frame to make ease of going up and down in long copied text
                scroll_bar = Scrollbar(text_frame) #vertical scrollbar  
                scroll_bar.pack(side = RIGHT, fill = Y)       
                
                #to paste copied text by user
                text = Text(text_frame, yscrollcommand = scroll_bar.set, height=25, padx=10,width=120)
                text.pack(fill=BOTH)

                text.insert("1.0", "{}".format( dict_of_elements[index_]))
                scroll_bar.config( command = text.yview )

                text_frame.pack(fill = BOTH)

                options_frame = Frame(main_frame,pady=10)


                Button(options_frame, text="Restore", justify=CENTER, 
                       command=lambda : In_out_recycle_bin_data.restore_(self, index_, dict_of_elements),
                       fg="white", relief=GROOVE, border=10,
                       bg="blue", height=1, width=10, font="lucida 15 bold").pack()
                
                Button(options_frame, text="Delete", justify=CENTER, 
                       command=lambda : In_out_recycle_bin_data.delete_(self, index_, dict_of_elements),
                       fg="white", relief=GROOVE, border=10,
                       bg="red", height=1, width=10, font="lucida 15 bold").pack()

                options_frame.pack()

                main_frame.pack()

            else:
                tmsg.showwarning("Error","Index you chosen {} is not in Data Display".format(index_))

        else:
            tmsg.showinfo('No Data',"There is no data")



    def recycle_bin_data_showing(self, dict_of_elements):
        
        global root

        if dict_of_elements:
            root.destroy()

            root = Tk()
            root.title("Data - Recycle Bin")
            root.geometry("1200x630")

            self.go_back_and_exit_menu(lambda : self.main_window( 0 ))

            heading_frame = Frame(root,bg="grey")
            Label(heading_frame,text="DATA DISPLAY", font='lucida 35 bold', justify='center', bg="grey").pack()
            heading_frame.pack(fill=X)


            main_frame = Frame(root)

            text_frame = Frame(main_frame,pady = 10, padx = 10)
            
            scroll_bar = Scrollbar(text_frame) #vertical scrollbar  
            scroll_bar.pack(side = RIGHT, fill = Y)       
            
            #to paste copied text by user
            text = Text(text_frame, yscrollcommand = scroll_bar.set, height=20)
            text.pack(fill=BOTH)

            for key in dict_of_elements:
                text.insert("1.0", "\n\n{}.\n{}".format(key, dict_of_elements[key]))
                text.insert("1.0", "\n"+"x"*60)

            scroll_bar.config( command = text.yview ) 

            text_frame.pack(fill = BOTH)


            option_frame = Frame(main_frame)

            Label(option_frame,
                text="Index of text if you want to select particular text else use given options",
                font='lucida 20 bold', justify='center').pack()

            index_ = IntVar(option_frame)

            index_entry = Entry(option_frame, textvariable = index_, relief = SUNKEN,font = "lucida 20 bold")
            index_entry.pack()
            
            Button(option_frame,text="Select",
                    command= lambda: self.options_for_recycle_bin_data(index_.get(), 
                                                                       dict_of_elements),
                    bg="blue", fg="white", justify=CENTER, height=1, width=10, relief=GROOVE,
                    border=10, font = "lucida 15 bold").pack(pady=10)

            Button(option_frame, text="Delete All",
                    command = lambda : In_out_recycle_bin_data.delete_all( self, dict_of_elements),
                    bg = "red", fg = "white", height=1, width = 12, relief = GROOVE,
                    border = 10, font = "lucida 15 bold").pack(pady=5, padx=10,side=RIGHT)

            Button(option_frame, text="Restore All",
                    command = lambda : In_out_recycle_bin_data.restore_all( self, dict_of_elements),
                    bg = "blue", fg = "white", height=1, width = 12, relief = GROOVE,
                    border = 10, font = "lucida 15 bold").pack(pady=5, padx=10,side=LEFT)

            option_frame.pack(side = BOTTOM, fill = BOTH)

            main_frame.pack(fill = BOTH)

        else:
            tmsg.showinfo("No data", "There is no data to show")



    


class Main_GUI( GUI_clip, GUI_Recycle ):

    def n_previous_copies(self):

        global root

        root.destroy()

        root = Tk()
        root.title("Fill n")

        self.go_back_and_exit_menu(lambda : self.main_window( 0 ))

        Label(root,text="Enter how many last stored element you want to use ?",font = "lucida 20 bold",
                justify = CENTER).pack(pady = 5)

        number_of_elements = IntVar(root)

        n_entry = Entry(root,textvariable = number_of_elements,justify = CENTER, font="lucida 20")
        n_entry.pack()

        Button(root, text="Proceed",
               command = lambda : In_out_clip_data.fetch_previous_n_saved(self,
                                                                          number_of_elements.get()),
                fg = "white", bg="blue", relief=GROOVE, border=10, height=1, width= 10,
                font = "lucida 15 bold", justify=CENTER).pack( pady=5 )

    def date_data(self, called_for):
        global root

        root.destroy()

        root = Tk()
        root.title("Ask Date")

        self.go_back_and_exit_menu(lambda : self.main_window( 0 ))

        Label(root, text="Enter a valid date(dd/mm/yyyy) to fetch detail of {}".format(called_for),
              font = "lucida 20", justify=CENTER).pack(pady = 5)

        date = StringVar(root)

        date_entry = Entry(root, textvariable = date, justify=CENTER, font="Lucida 15")
        date_entry.pack()

        if called_for == "Clip_board":
            function_call = lambda : In_out_clip_data.fetch_for_particular_date(self, date.get())
        else:
            function_call = lambda : In_out_recycle_bin_data.fetch_data_for_date(self, date.get())

        Button(root, text="Proceed",
               command = function_call,
                fg = "white", bg="blue", relief=GROOVE, border=10, height=1, width= 10,
                font = "lucida 15 bold", justify=CENTER).pack( pady=5 )


    def main_window(self, flag):

        global root

        if flag == 0:
            root.destroy()

        root = Tk()
        root.title("CLIP Board")
        root.geometry("600x500")


        heading_frame = Frame(root, bg="grey", pady=10)
        Label(heading_frame, text="Clip Board( fetch and use )", bg="grey", font="lucida 35 bold", justify=CENTER).pack()
        heading_frame.pack( fill=X )

        options_frame = Frame(root, pady=10)

        Button(options_frame, text="Previous n copies Data", height=1, width=20, relief=GROOVE, font = "lucida 20 bold",
                command = self.n_previous_copies,
                border = 10 ).pack(pady = 5)
        Button(options_frame, text="Date's clip data", height=1, width=20, relief=GROOVE, 
                command = lambda : self.date_data("Clip_board"),
                font = "lucida 20 bold", border = 10 ).pack(pady = 5)
        Button(options_frame, text="Recycle bin Data", height=1, width=20, relief=GROOVE,
                command = lambda : In_out_recycle_bin_data.fetch_all_data_recycle_bin(self),
                 font = "lucida 20 bold", border = 10 ).pack(pady = 5)
        Button(options_frame, text="Date's recycle bin data", height=1, width=20, relief=GROOVE,
                command = lambda : self.date_data("Recycle_bin"),
                 font = "lucida 20 bold", border = 10 ).pack(pady = 5)
        Button(options_frame, text="Exit", height=1, width=10, relief=GROOVE,
                command = quit, bg = "red", fg = "white",
                 font = "lucida 20 bold", border = 10 ).pack(pady = 5)

        options_frame.pack( fill=BOTH )
        


if __name__ == "__main__":

    obj = Main_GUI()
    obj.main_window(1)
    root.mainloop()