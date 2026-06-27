import os 
import sys
import json
import pandas as pd
import numpy as np
import pymongo
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

from dotenv import load_dotenv

load_dotenv()


MONGO_DB_URL = os.getenv('MONGO_URI')


import certifi
## Cerificate Authorities
ca = certifi.where()



class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def csv_to_json_covertor(self,filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True,inplace=True)
            reccords = list(json.loads(data.T.to_json()).values())
            return reccords
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


if __name__ == "__main__":
    filepath = 'Network_Data/phisingData.csv'
    DATABASE = 'NetworkSecurity'
    Collection = "NetworkData"

    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_covertor(filepath=filepath)
    print(records)
    no_of_records = network_obj.insert_data_mongodb(records=records,database=DATABASE,collection=Collection)
    print(no_of_records)