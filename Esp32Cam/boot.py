# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
#import webrepl
#webrepl.start()
from webcam import *
import _thread

import machine
import time
led = machine.Pin(4, machine.Pin.OUT)

def blink_led(num=1):
    for i in range(num):
        led.value(1)
        time.sleep(1)
        led.value(0)
    
#blink_led()

# set camera configuration
K.configure(camera, K.ai_thinker) # AI-Thinker PINs map - no need (default)
#camera.conf(K.XCLK_MHZ, 16) # 16Mhz xclk rate
camera.conf(K.XCLK_MHZ, 14) # 14Mhz xclk rate
#camera.conf(K.XCLK_MHZ, 13) # 14Mhz xclk rate
#camera.conf(K.XCLK_MHZ, 12) # 12Mhz xclk rate - to reduce "cam_hal: EV-EOF-OVF"

# wait for camera ready
for i in range(5):
    cam = camera.init()
    print("Camera ready?: ", cam)
    if cam:
        blink_led(3)
        break
    else: sleep(2)
else:
    print('Timeout')
    reset() 

if cam:
   print("Camera ready")
   # wait for wifi ready
   w = Sta()
   w.connect()
   w.wait()
   for i in range(5):
       if w.wlan.isconnected(): break
       else: print("WIFI not ready. Wait...");sleep(2)
   else:
      print("WIFI not ready. Can't continue!")
      reset()
      
blink_led(3)
# set auth
auth.on=False
#auth.on=False  # False: no authentication needed

if auth.on:
   auth.pwd=pwd()
   auth.ip=''
   print(f'PWD: {auth.pwd}')

# set preffered camera setting
camera.framesize(10)     # frame size 800X600 (1.33 espect ratio)
#camera.framesize(11)     
#camera.framesize(12)    
camera.quality(5)
#camera.quality(10)
camera.brightness(3)
camera.contrast(2)       # increase contrast
#camera.contrast(0)
camera.speffect(0)       # 2 jpeg grayscale

cam_setting['framesize']=10
cam_setting['quality']=5
cam_setting['contrast']=0
cam_setting['speffect']=2
cam_setting['brightness']=3

site.ip=w.wlan.ifconfig()[0]
site.camera=camera

server((80,))  # port 80
data = {"error": f"Reset data!"}
response = urequests.post(url, json=data)
response.close()
reset()


def thread_function():
    blink_led(2)
    
    while True:
        server((80,))  # port 80
        data = {"error": f"Reset data!"}
        response = urequests.post(url, json=data)
        response.close()
        reset()

try:
    #_thread.start_new_thread(thread_function, ())
    pass
except Exception as e:
    print('Error:', e)
    
server((80,))  # port 80
data = {"error": f"Reset data!"}
response = urequests.post(url, json=data)
response.close()
time.sleep(3)
reset()
