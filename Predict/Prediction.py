from pathlib import Path
import os
from pyexpat import model
import pandas as pd
import pickle
from sklearn.feature_selection import SelectFdr
from App_Logger.AppLogger import AppLogger
from Configuration.config import Config
from DataClear.DataCleaner import DataCleaner
from Modules.Modules import ModuleName
from PreProcesing.preprocessing import PreProcesing


class Prediction:
    def __init__(self) -> None:
        self.Logger= AppLogger()
        self.config= Config()
        self.createDummyDataFrame()

    def createDummyDataFrame(self):
        self.data_frame= pd.DataFrame(columns=['Age','Sex','On_Thyroxine','Query_On_Thyroxine','On_Antithyroid_Medication','Sick','Pregnant','Thyroid_Surgery',
        'I131_treatment',	'Query_Hypothyroid:','Query_Hyperthyroid','Lithium','Goitre','Tumor','Hypopituitary','Psych','TSH_Measured',
        'TSH','T3_Measured','T3','TT4_Measured','TT4','T4U_Measured','T4U',	'FTI_Measured','FTI','TBG_Measured','TBG','Referral_Source:'])

    def addDataToDataFrame(self, formdata):
        #print(formdata)
        #temp= pd.DataFrame(formdata,index=[0])
        #temp.set_index('index', drop=True, inplace=True)
        #print(temp.head())
        self.data_frame=self.data_frame.append(formdata, ignore_index=True)
        print(f"Head= {self.data_frame.head()}")
    
    def cleanTheData(self):
        data_cleaner=DataCleaner()
        data_cleaner.data_frame= self.data_frame.copy()
        data_cleaner.DropRefrenceColumn("Referral_Source:")
        data_cleaner.ReplaceQuestionMarkWithNaN()
    
        data_cleaner.ShapeofData()
        data_cleaner.ReplaceTValues()
        data_cleaner.ReplacefValues()
        data_cleaner.ConvertSexInNumbericForPredication()
        data_cleaner.measuredVsOriginal('TSH','TSH_Measured')
        data_cleaner.measuredVsOriginal('T3','T3_Measured')
        data_cleaner.measuredVsOriginal('TT4','TT4_Measured')
        data_cleaner.measuredVsOriginal('T4U','T4U_Measured')
        data_cleaner.measuredVsOriginal('FTI','FTI_Measured')
        data_cleaner.measuredVsOriginal('TBG','TBG_Measured')

        data_cleaner.DropRefrenceColumn("TSH_Measured")
        data_cleaner.DropRefrenceColumn("T3_Measured")
        data_cleaner.DropRefrenceColumn("TT4_Measured")
        data_cleaner.DropRefrenceColumn("T4U_Measured")
        data_cleaner.DropRefrenceColumn("FTI_Measured")
        data_cleaner.DropRefrenceColumn("TBG_Measured")

        #data_cleaner.CleaningTheOutPutVariable()
    

        data_cleaner.ReplaceNanWithZero()
        data_cleaner.DropNanValues()
        data_cleaner.ShapeofData()
        self.data_frame=self.convertTheColumnsintoInteger(data_cleaner.data_frame)
        self.data_frame= data_cleaner.data_frame

    def preProcessTheData(self):
        preprocess= PreProcesing()

        #preprocess.readCleanedDataSet()
        preprocess.data_frame= self.data_frame.copy()

        
        preprocess.CleanAgeUpperBoundData()
        preprocess.cleaningTheUpperBoundData("TBG", 50) #TBG values above 50 will be considered as 50
        preprocess.cleaningTheUpperBoundData("TSH", 5)  #TSH values above 5 will be considered as 5
        preprocess.cleaningTheUpperBoundData("T3", 5) #T3 values above 5 will be condered as 5
        preprocess.cleaningTheUpperBoundData("TT4", 175) #TT4 above 174 will be considered as 175
        preprocess.cleaningTheUpperBoundData("FTI", 200) # FTI above 200 will be considered as 200
        #Dropping the TBG columsn as most of the values are 0
        preprocess.DropRefrenceColumn("TBG")

        # Scalling the column between 0 and 1
        preprocess.ScaleTheData("TSH")
        preprocess.ScaleTheData("T3")
        preprocess.ScaleTheData("TT4")
        preprocess.ScaleTheData("FTI")
        self.data_frame=preprocess.data_frame

        #print(self.data_frame.head())
        #print(self.data_frame.dtypes)
    
    def convertTheColumnsintoInteger(self, dataframe):
        floatdatacolumsn=['TSH','T3','TT4','T4U','FTI','TBG']
        for i in dataframe.columns:
            if dataframe[i].dtype == "object":
                if i in floatdatacolumsn:
                    dataframe[i]= dataframe[i].astype(float)
                else:
                    dataframe[i]= dataframe[i].astype(int)
        return dataframe

    def getCluster(self):
        try:
            clusterModelPath = Path(f"{os.getcwd()}\\Models\\Clustering.pkl")

            with open(clusterModelPath, 'rb') as f:

                cluster_model=pickle.load(f)
                print(cluster_model.get_feature_names_out)
                print(self.data_frame.columns)
                cluster= cluster_model.predict(self.data_frame)
                self.Logger.log(ModuleName.Predict,f"Predicted Cluster is {cluster}")
                return cluster
        except Exception as e:
            self.Logger.log(ModuleName.Predict,f"Error Occured while Predicting Cluster !!! \n {e}")

    def getPredictedValue(self, cluster):
        output=[]
        if cluster ==0:
            output.append(self.predictUsingExtraTreeClassifier(0))
            output.append(self.predictUsingKNN(0))
            output.append(self.predictUsingRandomForest(0))

            return self.voteForTheOutput(output)
        elif cluster ==1:
            output.append(self.predictUsingExtraTreeClassifier(0))
            output.append(self.predictUsingKNN(0))
            output.append(self.predictUsingRandomForest(0))

            return self.voteForTheOutput(output)
        elif cluster ==2:
            output.append(self.predictUsingExtraTreeClassifier(0))
            output.append(self.predictUsingKNN(0))
            output.append(self.predictUsingRandomForest(0))

            return self.voteForTheOutput(output)
        elif cluster ==3:
            output.append(self.predictUsingExtraTreeClassifier(0))
            output.append(self.predictUsingKNN(0))
            output.append(self.predictUsingRandomForest(0))

            return self.voteForTheOutput(output)
        else:
            raise 

    def predictUsingExtraTreeClassifier(self, cluster):
        model_name= f"ExtraTreesClassifier_{cluster}"
        return self.loadModel(model_name)
    
    def predictUsingKNN(self, cluster):
        model_name= f"KNN_{cluster}"
        return self.loadModel(model_name)

    def predictUsingRandomForest(self, cluster):
        model_name= f"RandomForest_{cluster}"
        return self.loadModel(model_name)

    def loadModel(self,modelName):
        try:
            clusterModelPath = Path(f"{os.getcwd()}\\Models\\{modelName}.pkl")
            self.Logger.log(ModuleName.Predict,f"Loading Model {clusterModelPath}")
            with open(clusterModelPath, 'rb') as f:

                model=pickle.load(f)
                #print(cluster_model.get_feature_names_out)
                #print(self.data_frame.columns)
                data=self.data_frame[['TSH', 'T3', 'TT4', 'T4U','FTI','Age','On_Thyroxine','Pregnant','Sex','Lithium']]
                result= model.predict(data)
                self.Logger.log(ModuleName.Predict,f"Predicted outcome using model {model} is  {result} ")
                return result[0]
        except Exception as e:
            self.Logger.log(ModuleName.Predict,f"Error Occured while loading model {clusterModelPath} !!! \n {e}")

    def voteForTheOutput(self, arr):
        isPotive=0
        isNegative=0
        for i in arr:
            if i==0:
                isNegative+=1
            else:
                isPotive+=1
        if isPotive>isNegative:
            return True
        return False