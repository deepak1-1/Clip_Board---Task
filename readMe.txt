
Welcome to clip board read me file

- as you may have seen that there are 5 files with .py extension these are our python files and 2 out .txt 
 
 1. Bakend.py
 	- file can't be used independtly may lead some error
 	- implemented queries and function related to Main.py which will be called when user call any button or menu widget, some of functions it call is of
 	  "Main.py" file

 2. Database_connections.py
 	- the file need to be executed for the first time if you are running these all files for the first time so that it can create tables and you later 
 	  can enjoy it's features
    - it provide connections like cursor and connection to the database some basic functionality over database
    - so this is the main file imported in all files

3. Main.py
	- to use clip board functions GUI you can simply double click over the file and simple can use them
	- it provide function over both clip main data and recycle bin data 

4. Main_Script_backend.py
   	- this is the main script to run at backend but ya comment function Script.pasting_backend() so that the database will not be locked when you are using GUI
   	  or working with database
   	- don't worry we have provided a file "Manual_pasting.py" which will allow you to store your copied text and provide some other fuctions
   	- the other 2 methods needs to be executed every day so that they can perform there task (5 and 7 days back removal from recycle_bin and clip data)

5. Manual_pasting.py
	- it will provide you with GUI to manua copy your data and store it to the database you can edit that too
	- provides only 3 function in which 2 are quite similar


Hope you will enjoy using it 