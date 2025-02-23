from flask import Flask, request, jsonify
from model import Model

class Controller():
    def __init__(self):
        self._app = Flask(__name__)
        self.__model = Model()

        self._app.add_url_rule('/insert/data', view_func=self._insert_data, methods=['POST'])
        self._app.add_url_rule('/find/all/data', view_func=self._find_all_data, methods=['GET'])

    def _insert_data(self):
        try:
            data = request.get_json()
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            air_quality = data.get('air_quality')
            motion = data.get('motion')

            self.__model.insert_data(temperature, humidity, air_quality, motion)
            
            return jsonify({'message': 'Data saved successfully'}), 201
        except Exception as e:
            return str(e), 500
        
    def _find_all_data(self):
        try:
            data = self.__model.find_all_data()
            return jsonify(data), 201
        except Exception as e:
            return str(e), 500
        
        
    def run(self):
        self._app.run(host='0.0.0.0')
