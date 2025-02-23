# ESP32 IoT Sensor Monitoring System

A monitoring system that collects environmental data using ESP32 microcontroller and various sensors, then sends the data to both Ubidots IoT platform and a local Flask server with MongoDB database.

## Features

- Real-time monitoring of:
  - Temperature
  - Humidity
  - Air Quality
  - Motion Detection
- Data visualization through Ubidots platform
- Local data storage using MongoDB and processing using Flask server
- Efficient data transmission (only sends when values change)

## Hardware Requirements
- ESP32 Development Board
- DHT11 Temperature and Humidity Sensor
- MQ-135 Air Quality Sensor
- PIR Motion Sensor
- Necessary connecting wires

## Software Requirements

- MicroPython firmware on ESP32
- MongoDB Database (local or Atlas)
- Python dependencies (specified in requirements.txt):
  - Flask >= 2.0.0
  - pymongo >= 4.0.0
  - python-dotenv >= 0.19.0

## Setup Instructions

1. Install MicroPython firmware on your ESP32 board
2. Configure your WiFi credentials in the ESP32 code
3. Set up your Ubidots account and get your authentication token
4. Set up MongoDB:
   - Create a MongoDB database (local or Atlas)
   - Create a collection for sensor data
   - Get your MongoDB connection string
5. Create and activate a virtual environment:
```bash
python -m venv venv
./venv/bin/activate
```
6. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```
7. Create a ```.env``` file in the root directory with your MongoDB configuration:
```bash
CLIENT = your_mongodb_connection_string
DATABASE = your_database_name
COLLECTION = your_collection_name
```
8. Configure the Flask server URL in the ESP32 code
9. Upload the code to your ESP32 board
10. Run the Flask server ```main.py```

## Usage
1. Power up the ESP32 with all sensors connected
2. The device will automatically:
    - Connect to configured WiFi network
    - Start collecting sensor data
    - Send data to Ubidots platform
    - Send data to local Flask server
3. Monitor your data through:
    - Ubidots dashboard
    - MongoDB database
    - Local Flask server endpoint
