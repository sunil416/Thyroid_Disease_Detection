import os
from pathlib import Path
from flask import Flask

from App_Logger.AppLogger import AppLogger
from Configuration.config import Config
from DBConnector.DBConnector import MongoDbClient
from DataClear.DataCleaner import DataCleaner
from Modules.Modules import ModuleName
from flask_debugtoolbar import DebugToolbarExtension


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

if __name__ == "__main__":
    app.run(debug=True)