from flask import Flask

from App_Logger.AppLogger import AppLogger
from Modules.Modules import ModuleName

app = Flask(__name__)


@app.route("/")
def home():
    logger=AppLogger()
    logger.Log(ModuleName.General, "Started With home route")
    return "Hello, Welcome To Thyroid Prediction Project"