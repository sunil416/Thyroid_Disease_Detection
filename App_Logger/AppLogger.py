from datetime import datetime

from Modules.Modules import ModuleName

'''
    Author: Sunil Kumar
    File Name: App Logger .py
    Description: Helps in loggin the Logs related to the Application

'''


class AppLogger:

    # Default Constructor
    def __init__(self) -> None:
        self.now = ""
        self.date = ""
        self.time = ""

    def log(self, module, msg):
        self.now = datetime.now()
        self.date = self.now.date()
        self.time = self.now.strftime("%H:%M:%S")
        self.__load_module_log_file(module, msg)

    def __load_module_log_file(self, module, msg):
        match module:
            case ModuleName.General:
                self.__log_data_to_logs("./Logs/General/General_logs.txt", module, msg)
            case ModuleName.DataBase:
                self.__log_data_to_logs("./Logs/DataBase/DataBase_logs.txt", module, msg)
            case ModuleName.DataCleanr:
                self.__log_data_to_logs("./Logs/DataCleanr/Data_Cleaner.txt", module, msg)
            case ModuleName.PreProcessing:
                self.__log_data_to_logs("./Logs/PreProcesing/PreProcessing.txt", module, msg)
            case ModuleName.Training:
                self.__log_data_to_logs("./Logs/Training/Training.txt", module, msg)
            case ModuleName.Predict:
                self.__log_data_to_logs("./Logs/Prediction/Prediction.txt", module, msg)

    def __log_data_to_logs(self, file_path, module, msg):
        with open(file_path, "a+") as f:
            f.write(f"{self.date} - {self.time} - Module Name : {module.name}, Message : {msg}\n")
