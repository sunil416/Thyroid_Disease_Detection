from flask import Flask

from App_Logger.AppLogger import AppLogger
from Configuration.config import Config
from DBConnector.DBConnector import MongoDbClient
from Modules.Modules import ModuleName

app = Flask(__name__)


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