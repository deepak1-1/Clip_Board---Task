#Provide GUI options to some selected database entry by user 

#import Section
from Backend import *
# from tkinter import *
# import tkinter.messagebox as tmsg
# import pyperclip as pyc




class GUI_clip( In_out_clip_data ):

    def copied_element_options( self, index_, dict_of_elements ):
        
        global root

        if index_ in dict_of_elements.keys():
            # root.destroy()

            root = Tk()
            root.title("Options")
            root.geometry("1200x600")

            heading_frame = Frame(root,bg="grey")
            Label(heading_frame,text="You have selected under shown text, you directly can edit if you want", 
                 font='lucida 25 bold', justify='center', bg="grey").pack()
            heading_frame.pack(fill=X)

            main_frame = Frame(root)

            text_frame = Frame(main_frame,pady = 10, padx = 10)
            #adding scrollbar to text_frame to make ease of going up and down in long copied text
            scroll_bar = Scrollbar(main_frame) #vertical scrollbar  
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
                                                              text.get("1.0", "end")),
                   fg="white", relief=GROOVE, border=10,
                   bg="blue", height=1, width=10, font="lucida 15 bold").pack()
            
            Button(options_frame, text="Delete", justify=CENTER, 
                   command=lambda : In_out_clip_data.delete_(self, index_, dict_of_elements,
                                                              text.get("1.0", "end") ),
                   fg="white", relief=GROOVE, border=10,
                   bg="red", height=1, width=10, font="lucida 15 bold").pack()

            options_frame.pack()

            main_frame.pack()

        else:
            tmsg.showwarning("Error","Index you chosen{} is not in Data Display GUI".format(index_))



    def copied_element_showing(self, dict_of_elements):

        global root

        # root.destory()        

        root = Tk()
        root.title("Clip Board")
        root.geometry("1200x620")

        heading_frame = Frame(root,bg="grey")
        Label(heading_frame,text="DATA DISPLAY", font='lucida 35 bold', justify='center', bg="grey").pack()
        heading_frame.pack(fill=X)


        main_frame = Frame(root)

        text_frame = Frame(main_frame,pady = 10, padx = 10)
        #adding scrollbar to text_frame to make ease of going up and down in long copied text
        scroll_bar = Scrollbar(text_frame) #vertical scrollbar  
        scroll_bar.pack(side = RIGHT, fill = Y)       
        
        #to paste copied text by user
        text = Text(text_frame, yscrollcommand = scroll_bar.set)
        text.pack(fill=BOTH)

        for i in dict_of_elements:
            text.insert("1.0", "\n\n\r{}. {}".format(i, dict_of_elements[i]))
            text.insert("1.0", "\n"+"x"*30)

        scroll_bar.config( command = text.yview ) 

        text_frame.pack(fill = BOTH)


        select_frame = Frame(main_frame)

        Label(select_frame,text="Fill Index of text you want to select", font='lucida 20 bold',
                 justify='center').pack()

        index_ = IntVar(select_frame)

        index_entry = Entry(select_frame, textvariable = index_, relief = SUNKEN,font = "lucida 20 bold")
        index_entry.pack()
        
        Button(select_frame,text="Select",command= lambda: self.copied_element_options(index_.get(), 
                                                                                        dict_of_elements),
                bg="blue", fg="white", justify=CENTER, height=1, width=10, relief=GROOVE,
                border=10, font = "lucida 15 bold").pack(pady=10)

        select_frame.pack(side = BOTTOM, fill = BOTH)

        main_frame.pack(fill = BOTH)


class GUI_Recycle( In_out_recycle_bin_data ):
    pass


class Main_GUI( GUI_clip, GUI_Recycle ):
    pass


if __name__ == "__main__":
    obj = GUI_clip()
    obj.copied_element_showing( obj.fetch_previous_n_saved(2))

    root.mainloop()