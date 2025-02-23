from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from datetime import datetime
import os

class Model():
    def __init__(self):
        load_dotenv()
        self.__client = MongoClient(os.getenv('CLIENT'),  server_api=ServerApi('1'))
        try:
            self.__database = self.__client.get_database(os.getenv('DATABASE'))
            self.__collection = self.__database.get_collection(os.getenv('COLLECTION'))
        except Exception as e:
            print(f'Error: {e}')


    def insert_data(self, temperature, humidity, air_quality, motion):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

        data = {
            'year' : year,
            'month' : month,
            'day' : day,
            'hour' : hour,
            'minute' : minute,
            'data' : {
                'temperature': temperature,
                'humidity': humidity,
                'air_quality': air_quality,
                'motion': motion
                }
            }
        
        self.__collection.insert_one(data)
    
    def find_all_data(self):
        data = self.__collection.find({}, {'_id' : 0})
        data = list(data)
        return data