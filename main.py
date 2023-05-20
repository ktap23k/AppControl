from l298n import *
import network
from machine import Pin
import time
from barrier import *
import _thread

pin = Pin(2, Pin.OUT)

# connect to WiFi network
wifi_ssid = "Atuan"
wifi_password = "12345678"
sta_if = network.WLAN(network.STA_IF)

def connect_wifi(wifi_ssid, wifi_password):
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_ssid, wifi_password)
        while not sta_if.isconnected():
            pass

connect_wifi(wifi_ssid, wifi_password)
print('Network configuration:', sta_if.ifconfig())

def blink_led(pin, num=3):
    for _ in range(num):
        pin.on()
        time.sleep(0.5)
        pin.off()
        time.sleep(0.1)

blink_led(pin, 3)

def change_str_json(string):
    import ujson
    try:
        return ujson.loads(string)
    except Exception as e:
        print('error: ',e)
        return None

def speed_change(check, speed):
    if check == '{"data": "forward"}':
        forward(speed)
    elif check == '{"data": "backward"}':
        backward(speed)
    elif check == '{"data": "spin"}':
        spin(speed)
    

from async_websocket_client import AsyncWebsocketClient
import uasyncio as a
from random import randint

ws = AsyncWebsocketClient(5)

        
#_thread.start_new_thread(barrier, (sensor1, sensor2, sensor3, sensor4,))

async def connect():
    check = ''
    speed = 100
    print("...handshaked.")
    if not await ws.handshake("{}{}".format('ws://14.225.254.142:2024/', 12345)):
        raise Exception('Handshake error.')
    blink_led(pin, 2)
    print('check')
    while True:
        try:
            if ws is not None:
                if await ws.open():
                    #await ws.send()
                    data = await ws.recv()
                    if data:
                        if str(data) == '{"data": "forward"}' and check != '{"data": "forward"}':
                            check = '{"data": "forward"}'
                            pin.on()
                            forward(speed)
                            
                        elif str(data) == '{"data": "backward"}' and check != '{"data": "backward"}':
                            check = '{"data": "backward"}'
                            pin.on()
                            backward(speed)
                            
                        elif str(data) == '{"data": "spin"}' and check != '{"data": "spin"}':
                            check = '{"data": "spin"}'
                            pin.on()
                            spin(speed)
                        
                        elif str(data) == '{"data": "speed 1"}' and check != '{"data": "speed 1"}':
                            speed = 40
                            speed_change(check, speed)
                            check = '{"data": "speed 1"}'
                            
                        elif str(data) == '{"data": "speed 2"}' and check != '{"data": "speed 2"}':
                            speed = 70
                            speed_change(check, speed)
                            check = '{"data": "speed 2"}'

                        elif str(data) == '{"data": "speed 3"}' and check != '{"data": "speed 3"}':
                            speed = 100
                            speed_change(check, speed)
                            check = '{"data": "speed 3"}'
                            
                        elif str(data) == '{"data": "left"}' and check != '{"data": "left"}':
                            pin.on()
                            if check == '{"data": "forward"}':
                                left(speed//3)
                            elif check == '{"data": "backward"}':
                                left_(speed//3)
                            else:
                                move_left(speed)
                            check = '{"data": "left"}'
                            
                        elif str(data) == '{"data": "right"}' and check != '{"data": "right"}':
                            pin.on()
                            if check == '{"data": "forward"}':
                                right(speed//3)
                            elif check == '{"data": "backward"}':
                                right_(speed//3)
                            else:
                                move_right(speed)
                            check = '{"data": "right"}'
                            
                        elif str(data) == '{"data": "stop"}' and check != '{"data": "stop"}':
                            check = '{"data": "stop"}'
                            pin.off()
                            stop()
                        
                        elif str(data) == '{"data": "quit"' and check != '{"data": "quit"':
                            check = '{"data": "quit"'
                            stop()
                            await ws.close()
                            time.sleep(1)
                            print('quit')
                            break

        except Exception as e:
            print('error: ',e)
            blink_led(pin, 5)
            try:
                if await ws.open():
                    await ws.close()
                else:
                    if not await ws.handshake("{}{}".format('ws://14.225.254.142:2024/', 12345)):
                       raise Exception('Handshake error.')
            except Exception as e:
                print('error: ',e)
        
    print("...handshaked.")
    
#a.run(connect())

