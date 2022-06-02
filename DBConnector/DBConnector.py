
'''
    Author: Sunil Kumar
    File Name: DBConnector.py
    Description: Helps in DB realted CURD operation 

'''
from pymongo import MongoClient
import pymongo

from App_Logger.AppLogger import AppLogger
from Configuration.config import Config
from Modules.Modules import ModuleName
class MongoDbClient :
    
    def __init__(self) -> None:
        self.logger= AppLogger()
        self.database=self.get_database()
        

    def get_database(self):

        try:
            conf= Config()
            self.logger.log(ModuleName.DataBase, "Starting the Proccess of DB Connection")
            # Provide the mongodb atlas url to connect python to mongodb using pymongo
            
            CONNECTION_STRING = f"mongodb+srv://{conf.userName}:{conf.password}@cluster0.foxfn.mongodb.net/?retryWrites=true&w=majority"
            # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
            client = MongoClient(CONNECTION_STRING)
            # Create the database for our example (we will use the same database throughout the tutorial
            database= client[conf.database]
            self.logger.log(ModuleName.DataBase, f"Successfully stablished the DB connection. {database}\n")
            return database
        except :
            self.logger.log(ModuleName.DataBase, "Error Occusered Suring the DB Connection\n")
    
    def get_required_collection(self, collection_name):
        try:
            self.logger.log(ModuleName.DataBase, f"Getting the collection {collection_name}")
            self.collection=self.database[collection_name]
            self.logger.log(ModuleName.DataBase, f"Successfull in getting the collection {self.collection}")
        except:
            self.logger.log(ModuleName.DataBase, f"Erorr Getting the collection {collection_name}\n")
    
    def fetch_all_data_from_collection(self):
        return self.collection.find()