from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv('CLIENT'))
db = client[os.getenv('DATABASE')]
collection = db[os.getenv('COLLECTION')]

@app.route('/data', methods=['POST'])
def data():
    try:
        data = request.get_json()
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        air_quality = data.get('air_quality')
        motion = data.get('motion')
        
        data_sensor = {
            'temperature': temperature,
            'humidity': humidity,
            'air_quality': air_quality,
            'motion': motion,
            'timestamp': datetime.now()
        }
        
        collection.insert_one(data_sensor)
        
        return jsonify({'message': 'Data saved successfully'}), 201
    except Exception as e:
        return str(e), 500

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True) 