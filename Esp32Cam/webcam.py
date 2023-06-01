#
# The MIT License (MIT)
#
# Copyright (c) Sharil Tumin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-----------------------------------------------------------------------------

# webcam.py MVC - This is the controller C of MVC

from machine import reset
from time import sleep
import usocket as soc
import gc
#
import camera
import config as K
from wifi import Sta
from help import Setting as cam_setting
import site

import urequests
url = 'http://14.225.254.142:2024/12345'

gc.enable() # Enable automatic garbage collection

auth=site.auth
pwd=site.pwd

def clean_up(cs):
   cs.close() # flash buffer and close socket
   del cs
   # gc.collect()

def route(pm):
   cs,rq=pm
   pth='*NOP*'
   rqp = rq.split('/')
   rl=len(rqp)
   if rl==1: # ''
      pth='/';v=0
   elif rl==2: # '/', '/a'
      pth=f'/{rqp[1]}';v=0
   else: # '/a/v' '/a/v/w/....'
      pth=f'/{rqp[1]}'
      if rqp[1]=='login':
         v=rqp[2]
      else:
         try:
            v=int(rqp[2])
         except:
            v=0
            pth='*ERR*'
            print('Not an integer value', rqp[2])
   if pth in site.app:
      #print(pth, site.app[pth])
      site.app[pth](cs,v)
   elif pth=='*NOP*':
      site.NOP(cs)
   else:
      site.ERR(cs)
   clean_up(cs)

def server(pm):
  p=pm[0]
  ss=soc.socket(soc.AF_INET, soc.SOCK_STREAM)
  ss.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
  sa = ('0.0.0.0', p)
  ss.bind(sa)
  ss.listen(1) # serve 1 client at a time
  print("Start server", p)
  if auth.on:
     print(f"Try - http://{site.server}/login/{auth.pwd}")
     data = {"url": f"http://{site.server}/login/{auth.pwd}"}
     response = urequests.post(url, json=data)
     response.close()
  else:
     print(f"Try - http://{site.server}")
     while True:
         data = {"url": f"http://{site.server}/live"}
         response = urequests.post(url, json=data)
         if response.status_code == 200:
             response.close()
             break
         else:
             sleep(2)
  while True:
     ms='';rq=[]
     try:
        cs, ca = ss.accept()
     except:
        pass
     else:
        r=b'';e=''
        try:
           r = cs.recv(1024) 
        except Exception as e:
           print(f"EX:{e}")
           clean_up(cs)
        try:
           ms = r.decode()
           rq = ms.split(' ')
        except Exception as e:
           print(f"RQ:{ms} EX:{e}")
           clean_up(cs)
        else:
           if len(rq)>=2:
              print(ca, rq[:2])
              rv,ph=rq[:2]  # GET /path
              if not auth.on:
                 route((cs, ph))
                 continue
              elif auth.ip==ca[0]: # authenticated client
                 route((cs, ph))
                 continue
              elif ph.find('login/')>=0: # do login
                 site.client=ca[0]
                 route((cs, ph))
                 continue
              else:
                 # Unauthorized otherwise
                 site.NO(cs) 
                 clean_up(cs) 

