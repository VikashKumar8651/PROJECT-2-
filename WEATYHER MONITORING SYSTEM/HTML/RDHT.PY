RDHT.PY:- 
import time
import board
import adafruit_dht
from time import sleep
from gpiozero import Buzzer, InputDevice
import urllib.request
import time
import random
dhtDevice = adafruit_dht.DHT11(board.D4,use_pulseio=False)
buzz =Buzzer(13)
no_rain = InputDevice(18)

def buzz_now(iterations):
    for x in range(iterations):
        buzz.on()
        sleep(0.1)
        buzz.off()
        sleep(0.1)


def dht():
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        return temperature_c,humidity


    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        #continue
        return -1,-1
    except Exception as error:
        dhtDevice.exit()
        raise error
  
def thingspeak(temp,hum,rain):
    BASE_URL ="https://api.thingspeak.com/update?api_key=0X9AP9Q0E6WA2S4S&field1={}&field2={}&field3={}".format(temp,hum,rain)
    print(BASE_URL)
    data = urllib.request.urlopen(BASE_URL)
    print(data)

while True:
    temp,hum,rain=0,0,0
    if no_rain.is_active:
        print("no rain detected")
        rain=0
    if not no_rain.is_active:
        print("its raining - get washing in!")
        rain=1
        buzz_now(5)
    
    temp,hum=dht()
    time.sleep(1.0)
    thingspeak(temp,hum,rain)
