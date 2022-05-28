from datetime import datetime
from email import message
from imp import load_module
from sys import modules

from Modules.Modules import ModuleName

'''
    Author: Sunil Kumar
    File Name: App Logger .py
    Description: Helps in loggin the Logs related to the Application

'''

class AppLogger:

    #Default Constructor 
    def __init__(self) -> None:
        pass

    
    def Log(self, module, message):

        self.now=datetime.now()
        self.date = self.now.date()
        self.time= self.now.strftime("%H:%M:%S")
        self.__Load_Module_Log_File(module, message)

   
    def __Load_Module_Log_File(self, module, message):
        match module:
            case ModuleName.General:
                self.__Log_Data_To_Logs("./Logs/General/General_logs.txt", module, message)
        

    def __Log_Data_To_Logs(self, file_path,module,message):
       with open(file_path,"a+") as f:
           f.write(f"{self.date} - {self.time} - Module Name : {module.name}, Message : {message}\n")
    
