import os
from pathlib import Path
from flask import Flask, request, Response
from sklearn.metrics import precision_recall_curve

from App_Logger.AppLogger import AppLogger
from Configuration.config import Config
from DBConnector.DBConnector import MongoDbClient
from DataClear.DataCleaner import DataCleaner
from Modules.Modules import ModuleName
from flask_debugtoolbar import DebugToolbarExtension
import pandas as pd

from PreProcesing.preprocessing import PreProcesing
from Predict.Prediction import Prediction
from Training.training import Training


app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'

#toolbar = DebugToolbarExtension(app)

@app.route("/")
def home():
    logger=AppLogger()
    logger.log(ModuleName.General, "Started With home route")
    dbclient=MongoDbClient()
    conf=Config()
    dbclient.get_required_collection(conf.collection_student_details)
    data=dbclient.fetch_all_data_from_collection()
    for item in data:
        print(item)
    return "Hello, Welcome To Thyroid Prediction Project"

@app.route("/eda")
def eda():
    data_cleaner=DataCleaner()
    path=Path(f"{os.getcwd()}\\DataSource")
    file_name= "thyroid0387_data.xlsx"
    print(path)
    data_cleaner.ReadData(path, file_name)
    data_cleaner.ShapeofData()
    data_cleaner.DropRefrenceColumn("Referral_Source:")
    data_cleaner.ReplaceQuestionMarkWithNaN()
    
    data_cleaner.ShapeofData()
    data_cleaner.ReplaceTValues()
    data_cleaner.ReplacefValues()
    data_cleaner.ConvertSexInNumberic()
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

    data_cleaner.CleaningTheOutPutVariable()
    

    data_cleaner.ReplaceNanWithZero()
    data_cleaner.DropNanValues()
    data_cleaner.ShapeofData()
    data_cleaner.SaveTheCleanedData()

    return "Executed Succesffulyy"

@app.route('/preprocessing')
def preprocessing():
    preprocess= PreProcesing()

    preprocess.readCleanedDataSet()
    preprocess.createBinaryOutput()
    preprocess.convertOoutputtoLableEncoder()
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
    preprocess.creatingTheClusters()
    preprocess.SaveTheCleanedData()

    return "Preprocessing Done Successfully"

@app.route('/train')
def trainning():
    training= Training()
    training.createModelForKNN(0)
    training.createModelForExtraTreeClassifier(0)
    training.createModelForRandomForest(0)

    training.createModelForKNN(1)
    training.createModelForExtraTreeClassifier(1)
    training.createModelForRandomForest(1)

    training.createModelForKNN(2)
    training.createModelForExtraTreeClassifier(2)
    training.createModelForRandomForest(2)

    training.createModelForKNN(3)
    training.createModelForExtraTreeClassifier(3)
    training.createModelForRandomForest(3)

    return "Models Created Successfully"

@app.route('/predict', methods=['POST'])
def predict():
    #print(request.form['user'])
    predict=Prediction()
    li=[]
    #di={}
    #da=pd.DataFrame(request.form.items())
    #print(da.head())
    
    test_data_frame=pd.read_csv("D:\\Sunil Personal\\ML Books\\Learning\\Thyroid Disease Detection\\DataSource\\allrep.test.csv")
    original_out=test_data_frame['Output']
    test_data_frame.drop('Output', axis=1, inplace=True)
    for i in range(0,test_data_frame.shape[0]):
        di ={}
        for col_name in test_data_frame.columns:
            di.update({col_name:test_data_frame[col_name].iloc[i]})
        print(di)
        predict.createDummyDataFrame()
        predict.addDataToDataFrame(di)

        predict.cleanTheData()
        predict.preProcessTheData()
        li.append(predict.getPredictedValue(predict.getCluster()))
    test_data_frame["output"]= original_out
    test_data_frame['Yhat']=li

    test_data_frame.to_csv("D:\\Sunil Personal\\ML Books\\Learning\\Thyroid Disease Detection\\DataSource\\allrep.test_Predicted.csv")
    # for items in request.form.items():
    #      di.update({items[0]:items[1]})
    # predict.createDummyDataFrame()
    # predict.addDataToDataFrame(di)

    # predict.cleanTheData()
    # predict.preProcessTheData()
    #output=predict.getPredictedValue(predict.getCluster())
    #return f"Your Thyroid Status = {output}"

    return "Sucess"




if __name__ == "__main__":
    app.run(debug=True)