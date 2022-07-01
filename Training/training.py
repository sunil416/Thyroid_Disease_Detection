import pandas as pd
import os
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, f1_score, fbeta_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import pickle

from App_Logger.AppLogger import AppLogger
from Configuration.config import Config
from Modules.Modules import ModuleName


class Training:
    def __init__(self) -> None:
        self.Logger= AppLogger()
        self.config= Config()
        self.readCleanedDataSet()
        
    def readCleanedDataSet(self):
        file_path= Path(f"{os.getcwd()}\\DataSource\\PreProcesedData\\PreProcesedData.csv")
        try:
            self.Logger.log(ModuleName.Training,f"Reading the File {file_path}")
            self.data_frame=pd.read_csv(file_path)
            self.data_frame.set_index("Unnamed: 0", drop=True, inplace=True)
            self.Logger.log(ModuleName.Training,f"File {file_path} reading completed")
        except Exception as e:
            self.Logger.log(ModuleName.Training,f"Error Occured while Reading File \n {e}")
    
    def getBestParamters(self, estimator,params, X_train,y_train ):
        rf_random = GridSearchCV(estimator = estimator, param_grid = params, 
                               cv = 3, verbose=2,  n_jobs = -1)
        rf_random.fit(X_train,y_train)
        return rf_random.best_params_
    
    def claculateScore(self,y_test, y_hat):
        try:
            self.Logger.log(ModuleName.Training,f"Calculating Accuracy, F1 Score and FBeta Score")
            self.Logger.log(ModuleName.Training,f"Accuracy = {accuracy_score(y_test, y_hat)}")
            self.Logger.log(ModuleName.Training,f"F1 Score = {f1_score(y_test, y_hat)}")
            self.Logger.log(ModuleName.Training,f"FBeta Score = {fbeta_score(y_test, y_hat, beta=0.5)}")
            self.Logger.log(ModuleName.Training,f"Successfully calculated Accuracy, F1 Score and FBeta Score")
        except Exception as e:
            self.Logger.log(ModuleName.Training,f"Error Occured while calculating the Scores for the model \n {e}")

    def CreateDataForCluster(self,cluster_number):
        try:
            self.Logger.log(ModuleName.Training,f"Creating the data for the Cluster {cluster_number}")
            data_set_with_cluster=self.data_frame[self.data_frame["Cluster"]==cluster_number].copy()
            data_set_with_cluster.drop("Cluster", inplace=True, axis=1)
            self.Logger.log(ModuleName.Training,f"shape of the data = {data_set_with_cluster.shape}")
            y=data_set_with_cluster["Output_binary"]
            data_set_with_cluster.drop("Output", inplace=True, axis=1)
            data_set_with_cluster.drop("Output_binary", inplace=True, axis=1)
            data_set_with_cluster.drop("encoded_output", inplace=True, axis=1)
            #self.Logger.log(ModuleName.Training,f"{data_set_with_cluster.head()}")
            #data_set_with_cluster.set_index("Unnamed: 0", drop=True, inplace=True)
            X=data_set_with_cluster.copy()
            X=X[['TSH', 'T3', 'TT4', 'T4U','FTI','Age','On_Thyroxine','Pregnant','Sex','Lithium']]
            self.Logger.log(ModuleName.Training,f"Sucessfully created the data for the Cluster {cluster_number}")
            return train_test_split( X, y, test_size=0.25, random_state=42)
        except Exception as e:
            self.Logger.log(ModuleName.Training,f"Something went wrong !!! \n {e}")

    def saveModel(self, model_name, model):
        try:
            self.Logger.log(ModuleName.Training,f"Saving model = {model_name}")
            path_for_model= Path(f"{os.getcwd()}\\Models\\{model_name}.pkl")
            with path_for_model.open("wb") as f:
                pickle.dump(model,f)

            self.Logger.log(ModuleName.Training,f"Model = {model_name} saved successfully")
        
        except Exception as e:
            self.Logger.log(ModuleName.Training,f"Error Occured while saving the model {model_name} \n {e}")

    def createModelForRandomForest(self, cluster):
        try:
            X_train, X_test, y_train, y_test = self.CreateDataForCluster(cluster)
            params={
                'n_estimators':[100,200,300,10,50],
                'max_depth':[3,4,5,6,7,8,9,10]
            }

            best_params= self.getBestParamters(RandomForestClassifier(), params,  X_train, y_train)

            self.Logger.log(ModuleName.Training,f"Creating Random Forest Model for Cluster = {cluster} with params = {best_params}")
            rfc=RandomForestClassifier(n_estimators= best_params['n_estimators'], max_depth= best_params['max_depth'])
            rfc.fit(X_train, y_train)
            y_hat=rfc.predict(X_test)
            self.claculateScore(y_test, y_hat)
            self.saveModel(f"RandomForest_{cluster}",rfc)
            self.Logger.log(ModuleName.Training,f"Model Creating Success !!!!!")
        except Exception as e:
            self.Logger.log(ModuleName.Training,f"Error Occured while creating Random Forest Model !!! \n {e}")
    
    def createModelForKNN(self, cluster):
        try:
            X_train, X_test, y_train, y_test = self.CreateDataForCluster(cluster)
            params={
                'n_neighbors':[2,3,4,5,6,7,8,9,10],
                'weights':['uniform','distance'],
                'algorithm':['auto', 'ball_tree', 'kd_tree', 'brute'],
                'leaf_size':[5,10,15,20,25,30,35,40]
            }

            best_params= self.getBestParamters(KNeighborsClassifier(), params,  X_train, y_train)
            
            self.Logger.log(ModuleName.Training,f"Creating KNN Model for Cluster = {cluster} with params = {best_params}")
            rfc=KNeighborsClassifier(n_neighbors= best_params['n_neighbors'], weights= best_params['weights'],
                             algorithm= best_params['algorithm'],leaf_size= best_params['leaf_size'])
            rfc.fit(X_train, y_train)
            y_hat=rfc.predict(X_test)
            self.claculateScore(y_test, y_hat)
            self.saveModel(f"KNN_{cluster}",rfc)
            self.Logger.log(ModuleName.Training,f"Model Creating Success !!!!!")
        except Exception as e:
            self.Logger.log(ModuleName.Training,f"Error Occured while creating KNeighborsClassifier Model !!! \n {e}")
    
    def createModelForExtraTreeClassifier(self, cluster):
        try:
            X_train, X_test, y_train, y_test = self.CreateDataForCluster(cluster)
            params={
                'n_estimators':[100,200,300,10,50],
                'max_depth':[3,4,5,6,7,8,9,10]
            }

            best_params= self.getBestParamters(ExtraTreesClassifier(), params,  X_train, y_train)

            self.Logger.log(ModuleName.Training,f"Creating Extra Tree Classifier for Cluster = {cluster} with params = {best_params}")
            rfc=ExtraTreesClassifier(n_estimators= best_params['n_estimators'], max_depth= best_params['max_depth'])
            rfc.fit(X_train, y_train)
            y_hat=rfc.predict(X_test)
            self.claculateScore(y_test, y_hat)
            self.saveModel(f"ExtraTreesClassifier_{cluster}",rfc)
            self.Logger.log(ModuleName.Training,f"Model Creating Success !!!!!")
        except Exception as e:
            self.Logger.log(ModuleName.Training,f"Error Occured while creating ExtraTreesClassifier Model !!! \n {e}")