welcomeMessage = """
--------------------------------------------------------------------------------------------
Welcome to \033[1moscilloscopy\033[0m.
A software created to quickly interact with the oscilloscope
of the Povo 0 electronics laboratory at the Unitn.
--------------------------------------------------------------------------------------------
        """
helpMessage = """
---- COMMAND LIST ------------------------------------------------------------------------- 

Change Filename: .csv file are saved by default in the \033[1mfiles\033[0mdirectory. 
                 You can choose to customize the default file name. There isn't
                 any safety check on the file name.                    
Read Data:       Read data from the oscilloscope via HTTP request in a fancy way. 
                 The ip address of your oscilloscope must be previously 
                 written in settings.json under the \033[1mip_oscilloscope\033[0m key.
                 If there is not connection the app will crash.
                 Read data will create \033[1mn_file\033[0m files each with 
                 \033[1mn_acquisitions\033[0m data rows. 
Change Settings: If don't want to edit the settings.json file directly you
                 can do it here.
Load Settings:   Load the settings.json with the newest settings.
Exit:            Blow up your command prompt.

--------------------------------------------------------------------------------------------

NB: url_csv, url_file and url_ws in settings.json are not meant to be edited. Be carefull.
Do it only if you know what you are doing.

--------------------------------------------------------------------------------------------
"""
