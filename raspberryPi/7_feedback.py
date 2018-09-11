import requests
import RPi.GPIO
import time
import datetime
from flask import Flask, request
import thread

GPIO_DHT11 = 20
GPIO_LED = 11
SLEEP_SECOND = 2
LED_OPENED = False
REMOTE_SERVER_URL = "http://192.168.137.1:8000/data"

app = Flask(__name__)

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_LED, RPi.GPIO.OUT)

def setupDHT11():
    RPi.GPIO.setup(GPIO_DHT11, RPi.GPIO.OUT)
    RPi.GPIO.output(GPIO_DHT11, RPi.GPIO.LOW)
    time.sleep(0.02)
    RPi.GPIO.output(GPIO_DHT11, RPi.GPIO.HIGH)
    RPi.GPIO.setup(GPIO_DHT11, RPi.GPIO.IN)

def read():
    data = []
    while RPi.GPIO.input(GPIO_DHT11) == RPi.GPIO.LOW:
        continue
    while RPi.GPIO.input(GPIO_DHT11) == RPi.GPIO.HIGH:
        continue
    j = 0
    while j < 40:
        k = 0
        while RPi.GPIO.input(GPIO_DHT11) == RPi.GPIO.LOW:
            continue
        while RPi.GPIO.input(GPIO_DHT11) == RPi.GPIO.HIGH:
            k += 1
            if k > 100:
                break
        if k < 8:
            data.append(0)
        else:
            data.append(1)
        j += 1
    return data

def checkData(data):
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]
    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0
    for i in range(8):
        humidity += humidity_bit[i] * 2 ** (7-i)
        humidity_point += humidity_point_bit[i] * 2 ** (7-i)
        temperature += temperature_bit[i] * 2 ** (7-i)
        temperature_point += temperature_point_bit[i] * 2 ** (7-i)
        check += check_bit[i] * 2 ** (7-i)
    tmp = humidity + humidity_point + temperature + temperature_point
    if check == tmp:
        print("temperature :{0} C, humidity :{1} %%".format(temperature, humidity))
        return temperature, humidity
    else:
        print("got wrong data now")
    return None, None

def getValue(name, value):
    global LED_OPENED
    while LED_OPENED:
        setupDHT11()
        data = read()
        temperature, humidity = checkData(data)
        if temperature != None:
            send_data = {"t":temperature, "h":humidity}
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            print("time: " + str(datetime.datetime.now()))
            print("send {0}".format(send_data))
        time.sleep(SLEEP_SECOND)

@app.route('/', methods=['GET'])
def index():
    global LED_OPENED
    if 'op' in request.args:
        if request.args['op'] == "on" and not LED_OPENED:
            RPi.GPIO.output(GPIO_LED, RPi.GPIO.HIGH)
            LED_OPENED = True
            thread.start_new_thread(getValue, ("getValue", None))

        elif request.args['op'] == "off" and LED_OPENED:
            RPi.GPIO.output(GPIO_LED, RPi.GPIO.LOW)
            LED_OPENED = False
    return 'ok'

app.run(host='0.0.0.0')

