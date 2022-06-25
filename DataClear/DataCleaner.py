from importlib.resources import path
from logging import Logger
from pathlib import Path
import pandas as pd
from App_Logger.AppLogger import AppLogger
from Modules.Modules import ModuleName
import numpy as np
import os
from sklearn.impute import KNNImputer
class DataCleaner:

    # __singleton_lock = threading.Lock()
    # __singleton_instance = None
 
    # # define the classmethod
    # @classmethod
    # def instance(self):
 
    #     # check for the singleton instance
    #     if not self.__singleton_instance:
    #         with self.__singleton_lock:
    #             if not self.__singleton_instance:
    #                 self.__singleton_instance = DataCleaner()
 
    #     # return the singleton instance
    #     return self.__singleton_instance
    def __init__(self) -> None:
        self.Logger= AppLogger()

    def ReadData(self,path, fileName):
        file_path= Path(f"{path}\\{fileName}")
        try:
            self.Logger.log(ModuleName.DataCleanr,f"Reading the File {file_path}")
            self.data_frame=pd.read_excel(file_path)
            self.Logger.log(ModuleName.DataCleanr,f"File {file_path} reading completed")
        except Exception as e:
            self.Logger.log(ModuleName.DataCleanr,f"Error Occured while Reading File \n {e}")

    def DropRefrenceColumn(self, column_name):
        self.Logger.log(ModuleName.DataCleanr,f"Request to drop Column Name: {column_name}")
        try:
            self.data_frame.drop(column_name, inplace=True, axis=1)
            self.Logger.log(ModuleName.DataCleanr,f"Column Name: {column_name} Dropped Successfuly")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured while droping column {e}")

    def ReplaceQuestionMarkWithNaN(self):
        self.Logger.log(ModuleName.DataCleanr,f"Replacing the Question Mark with NAN")
        try:
            self.data_frame.replace("?",np.nan, inplace=True)
            self.Logger.log(ModuleName.DataCleanr,f"Successfuly")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured while replacing the data {e}")
    
    def DropNanValues(self):
        self.Logger.log(ModuleName.DataCleanr,f"Droping the Nan Values ")
        try:
            self.Logger.log(ModuleName.DataCleanr,f"{self.data_frame.isna().sum()}")
            self.data_frame.dropna(inplace=True)
            self.Logger.log(ModuleName.DataCleanr,f"Successfuly")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured while dropoing Nan values {e}")

    def ReplaceTValues(self ):
        self.Logger.log(ModuleName.DataCleanr,f"Replacing t with 1 ")
        try:
            self.data_frame.replace("t",1,inplace=True)
            self.Logger.log(ModuleName.DataCleanr,f"Successfuly")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured while replacing t values {e}")
    
    def ReplacefValues(self ):
        self.Logger.log(ModuleName.DataCleanr,f"Replacing f with 0 ")
        try:
            self.data_frame.replace("f",0,inplace=True)
            self.Logger.log(ModuleName.DataCleanr,f"Successfuly")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured while replacing f values {e}")
    
    def ConvertSexInNumberic(self):
        self.Logger.log(ModuleName.DataCleanr,f"Converting Sex into Numeric Column called Male ")
        try:
            dummeis=pd.get_dummies(self.data_frame["Sex"])
            self.Logger.log(ModuleName.DataCleanr,f"Successfully created the Dummies ")
            #if dummeis.shape[1]>=3:
            for i in range(0, dummeis.shape[0]):
                if dummeis['M'].iloc[i] ==1:
                    self.data_frame["Sex"].iloc[i]=dummeis['M'].iloc[i]
                elif dummeis['F'].iloc[i] ==1:
                    self.data_frame["Sex"].iloc[i]=dummeis['M'].iloc[i]
                else:
                    self.data_frame["Sex"].iloc[i] =np.nan
            if self.data_frame["Sex"].isna().sum()>0:

                knnimputer=KNNImputer(n_neighbors=3)
                self.data_frame=pd.DataFrame(knnimputer.fit_transform(self.data_frame), columns=self.data_frame.columns)
                self.Logger.log(ModuleName.DataCleanr,f"updated the Missing values using KNN column Sex ")
                self.data_frame["Sex"]= self.data_frame["Sex"].astype(int)

            self.Logger.log(ModuleName.DataCleanr,f"updated the values of the dumies in the column Sex ")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured Converting the sex into the numeric values {e}")
    
    def measuredVsOriginal(self,column_name, measured_Name):
        self.Logger.log(ModuleName.DataCleanr,f"Updateing the missing values of the measured {measured_Name} vs value {column_name}")
        try:
            for i in range(0, self.data_frame.shape[0]):
                if pd.isna(self.data_frame[column_name].iloc[i]) and self.data_frame[measured_Name].iloc[i]=='f':
                    self.data_frame[column_name].iloc[i]=0
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured updating the missing values for column {column_name} {e}")


    def CleaningTheOutPutVariable(self):

        self.Logger.log(ModuleName.DataCleanr,f"Cleaning the output variable ")
        try:
            output=[]
            for item in self.data_frame["Output"]:
                output.append(item[0:1])
            self.data_frame["Output"] =output
            self.Logger.log(ModuleName.DataCleanr,f"cleanend the Output variable ")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured while cleaning the output data {e}")

    def SaveTheCleanedData(self):
        self.Logger.log(ModuleName.DataCleanr,f"saving the cleaned Data ")
        try:
            path= Path(f"{os.getcwd()}\\DataSource\\CleanedData\\cleanedData.csv")
            self.data_frame.to_csv(path)
            self.Logger.log(ModuleName.DataCleanr,f"file Saved Successfully at path {path}")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured while saving Cleaned data {e}")

    def ReplaceNanWithZero(self):
        self.Logger.log(ModuleName.DataCleanr,f"Replacing Nan with 0 ")
        try:
           self.data_frame.fillna(0, inplace=True)
           self.Logger.log(ModuleName.DataCleanr,f"Success")
        except Exception as e:
             self.Logger.log(ModuleName.DataCleanr,f"Error occured while saving Cleaned data {e}")

    def ShapeofData(self):
        self.Logger.log(ModuleName.DataCleanr,f"Shape of the data =  {self.data_frame.shape}")
