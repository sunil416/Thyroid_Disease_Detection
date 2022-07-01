from pathlib import Path
import os
import pandas as pd
from App_Logger.AppLogger import AppLogger
from Configuration.config import Config
from Modules.Modules import  ModuleName
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.cluster import KMeans
import pickle



class PreProcesing:

    def __init__(self) -> None:
        self.Logger= AppLogger()
        self.config= Config()
        self.readCleanedDataSet()

    def readCleanedDataSet(self):
        file_path= Path(f"{os.getcwd()}\\DataSource\\CleanedData\\cleanedData.csv")
        try:
            self.Logger.log(ModuleName.PreProcessing,f"Reading the File {file_path}")
            self.data_frame=pd.read_csv(file_path)
            self.data_frame.set_index("Unnamed: 0", drop=True, inplace=True)
            self.Logger.log(ModuleName.PreProcessing,f"File {file_path} reading completed")
        except Exception as e:
            self.Logger.log(ModuleName.PreProcessing,f"Error Occured while Reading File \n {e}")


    def createBinaryOutput(self):
        try:
            self.Logger.log(ModuleName.PreProcessing,f"Creating the binary output")
            self.data_frame["Output_binary"]= self.data_frame["Output"]!='-'
            self.data_frame["Output_binary"]= self.data_frame["Output_binary"].astype(int)
            self.Logger.log(ModuleName.PreProcessing,f"Binary output created successfullly")
        except Exception as e:
             self.Logger.log(ModuleName.PreProcessing,f"Error Occured while Creating Binary Output \n {e}")
    
   

    def convertOoutputtoLableEncoder(self):
        try:
            self.Logger.log(ModuleName.PreProcessing,f"Creating Lables for output Variables")
            lblenc=LabelEncoder()
            self.data_frame["encoded_output"]=lblenc.fit_transform(self.data_frame["Output"])
            self.Logger.log(ModuleName.PreProcessing,f"Creating Lables for output Variables Success")
        except Exception as e:
             self.Logger.log(ModuleName.PreProcessing,f"Error Occured while Creating Label output cariables \n {e}")
    
    
    def CleanAgeUpperBoundData(self):
        try:
            self.Logger.log(ModuleName.PreProcessing,f"Droping the Data for the patients above age of 90")
            orignal_size=self.data_frame.shape[0]
            data_to_be_deleted=self.data_frame[self.data_frame['Age']>self.config.MaxAgeOfThePatient]
            self.data_frame.drop(data_to_be_deleted.index,inplace=True )
            size_changes=self.data_frame.shape[0]

            if orignal_size != size_changes:
                self.Logger.log(ModuleName.PreProcessing,f"No. of patients deleted are {orignal_size-size_changes}")
                self.Logger.log(ModuleName.PreProcessing,f"Below are the row delted \n {data_to_be_deleted}")
                self.Logger.log(ModuleName.PreProcessing,f"Dropped Successfully")
                return
            self.Logger.log(ModuleName.PreProcessing,f"No Data to remove")
        except Exception as e:
             self.Logger.log(ModuleName.PreProcessing,f"Error Occured while cleaning the upper bound of the Age data \n {e}")

    def cleaningTheUpperBoundData(self,column_name, upperBound):
        try:
            self.Logger.log(ModuleName.PreProcessing,f"Cleaning the upper bound data for {column_name}, and upper bound is {upperBound}")
            for i in range(0,self.data_frame.shape[0]):
                if self.data_frame[column_name].iloc[i] > upperBound:
                    self.Logger.log(ModuleName.PreProcessing,f"Updating the data for \n {self.data_frame.iloc[i]}")
                    old_data=self.data_frame[column_name].iloc[i]
                    self.data_frame[column_name].iloc[i]=upperBound
                    self.Logger.log(ModuleName.PreProcessing,f"Coulumn {column_name} Updated Successfully from {old_data} to {upperBound} ")
            self.Logger.log(ModuleName.PreProcessing,f"Executed Successfully")
        except Exception as e:
             self.Logger.log(ModuleName.PreProcessing,f"Error Occured while cleaning the upper bound of {column_name} \n {e}")

    def DropRefrenceColumn(self, column_name):
        self.Logger.log(ModuleName.PreProcessing,f"Request to drop Column Name: {column_name}")
        try:
            self.data_frame.drop(column_name, inplace=True, axis=1)
            self.Logger.log(ModuleName.PreProcessing,f"Column Name: {column_name} Dropped Successfuly")
        except Exception as e:
             self.Logger.log(ModuleName.PreProcessing,f"Error occured while droping column {e}")

    def ScaleTheData(self, column_name):
        self.Logger.log(ModuleName.PreProcessing,f"Scaling the data between 0 and 1 for the column {column_name} ")
        try:
            minMaxScaler= MinMaxScaler()
            array=self.data_frame[column_name].array
            scaller_data=minMaxScaler.fit_transform(array.reshape(-1,1))
            self.data_frame[column_name]=scaller_data
            self.Logger.log(ModuleName.PreProcessing,f"Scalling completed Successfully {column_name} ")
        except Exception as e:
             self.Logger.log(ModuleName.PreProcessing,f"Scaling failed {e}")
             raise 

    def creatingTheClusters(self):

        self.Logger.log(ModuleName.PreProcessing,f"Creating the Clusters for the data ")
        try:
            dataframe_Copy=self.data_frame.copy()
            dataframe_Copy.drop(["Output","Output_binary","encoded_output"], inplace= True, axis=1)
            kmeans=KMeans(n_clusters=4)
            model=kmeans.fit(dataframe_Copy)
            model_path = Path(f"{os.getcwd()}\\Models\\Clustering.pkl")
            with model_path.open('wb') as fp:
                pickle.dump(model, fp)
            dataframe_Copy["Cluster"]= kmeans.fit_predict(dataframe_Copy)
            dataframe_Copy["Output"]= self.data_frame["Output"]
            dataframe_Copy["Output_binary"]=self.data_frame["Output_binary"]
            dataframe_Copy["encoded_output"]=self.data_frame["encoded_output"]
            self.data_frame= dataframe_Copy
            self.Logger.log(ModuleName.PreProcessing,f"Success and dumped the model in the models folder ")
        except Exception as e:
             self.Logger.log(ModuleName.PreProcessing,f"creating cluster failed {e}")
             raise e

    def SaveTheCleanedData(self):
        self.Logger.log(ModuleName.PreProcessing,f"saving the cleaned Data ")
        try:
            path= Path(f"{os.getcwd()}\\DataSource\\PreProcesedData\\PreProcesedData.csv")
            self.data_frame.to_csv(path)
            self.Logger.log(ModuleName.PreProcessing,f"file Saved Successfully at path {path}")
        except Exception as e:
             self.Logger.log(ModuleName.PreProcessing,f"Error occured while saving Cleaned data {e}")
    

