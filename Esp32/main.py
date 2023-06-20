from l298n import *
import network
from machine import Pin, PWM
import time
from barrier import *
import _thread

#play sound
p23 = Pin(23, Pin.OUT)
buzzer = PWM(p23)
buzzer.freq(1047)

buzzer.duty(70)
time.sleep(0.5)
buzzer.duty(0)

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

def barrier(sensor1, sensor2, sensor3, sensor4, ws):
    def play_sound():
        buzzer.duty(70)
        time.sleep(0.3)
        buzzer.duty(0)

    async def send_data(ws):
        if ws is not None:
            if await ws.open():
                await ws.send("ESP32 connect!")
        while True:
            try:
                sau = sensor1.distance_cm()
                time.sleep(0.1)
                phai = sensor2.distance_cm()
                time.sleep(0.1)
                truoc = sensor3.distance_cm()
                time.sleep(0.1)
                trai = sensor4.distance_cm()
                if (sau > 2 and sau < 20) or \
                   (phai > 2 and phai < 20) or \
                   (truoc > 2 and truoc < 20) or \
                   (trai > 2 and trai < 20):
                        play_sound()
                        
                if (sau > 2 and sau < 10) or \
                   (phai > 2 and phai < 10) or \
                   (truoc > 2 and truoc < 10) or \
                   (trai > 2 and trai < 10):
                        pin.off()
                        stop()
                
                if (sau > 2 and sau < 125) or \
                   (phai > 2 and phai < 125) or \
                   (truoc > 2 and truoc < 125) or \
                   (trai > 2 and trai < 125):
                        time.sleep(0.5)
                        if ws is not None:
                            if await ws.open():
                                await ws.send(f"{sau} {phai} {truoc} {trai}")
                                #print('send: ', distance1, distance2, distance3, distance4)
            except Exception as e:
                print('error: ',e)
        
    loop = a.get_event_loop()
    loop.run_until_complete(send_data(ws))

async def connect():
    check = ''
    speed = 100
    print("...handshaked.")
    if not await ws.handshake("{}{}".format('ws://14.225.254.142:2024/', 12345)):
        raise Exception('Handshake error.')
    blink_led(pin, 2)
    _thread.start_new_thread(barrier, (sensor1, sensor2, sensor3, sensor4, ws, ))

    print('check')
    while True:
        try:
            if ws is not None:
                if await ws.open():
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
    
a.run(connect())

