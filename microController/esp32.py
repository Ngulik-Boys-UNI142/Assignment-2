import network
import urequests
import ujson
import time
import dht
from machine import Pin, ADC

# Konfigurasi Wifi
SSID = "Toko Kopi Jaya Ijen Lt 1"
PASSWORD = "Berjayabersama"

# Konfigurasi Ubidots
TOKEN = "BBUS-reJzd1NY4DgL646T8huuohOVENRTrY"
DEVICE_LABEL = "esp32-sensors"
VARIABLE_TEMP = "temperature"
VARIABLE_HUM = "humidity"
VARIABLE_AIR = "air_quality"
VARIABLE_PIR = "motion"

# Konfigurasi Flask
FLASK_SERVER_URL = "http://192.168.18.116:5000/data"

# PIN SENSOR
DHT_PIN = 5
MQ135_PIN = 34
PIR_PIN = 4

# Koneksi ke WiFi dengan timeout
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    timeout = 15
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("Terhubung ke WiFi!")
    else:
        print("Gagal terhubung ke WiFi!")

# Kirim data ke Ubidots
def send_to_ubidots(temp, hum, air_quality, motion):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    payload = {
        VARIABLE_TEMP: temp,
        VARIABLE_HUM: hum,
        VARIABLE_AIR: air_quality,
        VARIABLE_PIR: motion
    }
    try:
        response = urequests.post(url, json=payload, headers=headers)
        print("Response:", response.text)
        response.close()
    except Exception as e:
        print("Gagal mengirim data ke Ubidots:", e)

# Kirim Data ke FLask
def send_to_flask(temp, hum, air_quality, motion):
    payload = ujson.dumps({"temperature": temp, "humidity": hum, "air_quality": air_quality, "motion": motion})
    headers = {"Content-Type": "application/json"}
    try:
        response = urequests.post(FLASK_SERVER_URL, headers=headers, data=payload)
        print("Flask response: ", response.text)
        response.close()
    except Exception as e:
        print ("Gagal mengirim data ke flask: ", e)

# Inisialisasi sensor
connect_wifi()
sensor_dht = dht.DHT11(Pin(DHT_PIN))
sensor_mq135 = ADC(Pin(MQ135_PIN))
sensor_mq135.atten(ADC.ATTN_11DB)
sensor_pir = Pin(PIR_PIN, Pin.IN)

prev_temp = None
prev_hum = None
prev_air_quality = None
prev_motion = None

while True:
    try:
        # DHT11 Sensor
        temp, hum, air_quality, motion = None, None, None, None
        for _ in range(3):
            try:
                sensor_dht.measure()
                temp = sensor_dht.temperature()
                hum = sensor_dht.humidity()
                break
            except Exception:
                time.sleep(2)

        # MQ-135 Sensor
        air_quality = sensor_mq135.read()
        air_quality = (air_quality / 4095) * 100

        #Pir Sensor
        motion = sensor_pir.value()

        if (prev_temp != temp or prev_hum != hum or prev_air_quality != air_quality or prev_motion != motion):
            print(f"Suhu: {temp}°C, Kelembaban: {hum}%, Kualitas Udara: {air_quality}%, Gerakan: {motion}")
            send_to_ubidots(temp, hum, air_quality, motion)
            send_to_flask(temp, hum, air_quality, motion)

        prev_temp = temp
        prev_hum = hum
        prev_air_quality = air_quality
        prev_motion = motion
    except Exception as e:
        print("Error:", e)

    time.sleep(10)
