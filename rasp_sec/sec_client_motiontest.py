# Script to easy the testing of the implementation of the colortracking

import websocket
import thread
import time
import subprocess
import signal
import os
import re
#import colortracker as colortracker
import motioncolor
print "Secondary client running"
import thread
from multiprocessing import Process
#print "Secondary client running"
global track
def tracking(ws):
        xp = 1500
        yp = 1500
        px= 0.3
        py= 0.2
        dx= 0.5
        dy= 0.5
        x = 0
        y = 0
        motioncolor.init()
        start = time.time()
        while time.time()-start <= 10:
            tempx = x
            tempy = y
            [x,y] =motioncolor.getdata()
            xp=min(max(500,xp-x*px-(x-tempx)*dx),2500)
            yp=min(max(500,yp+y*py+(y-tempy)*dy),2500)
            #yp=yp-y*p
            xpos = str(int(xp))
            ypos = str(int(yp))
            ws.send(ypos+','+xpos+',1500,/n')
        thread.exit()

def on_message(ws, message):
    global pro
    print message
    if message[0:13] == "start_stream:":
        ip = re.search("start_stream:(.+?)#", message).group(1)
        pro = subprocess.Popen(['bash', 'camerastream.sh', ip], preexec_fn=os.setsid)
    elif message =="stop_stream":
        os.killpg(pro.pid, signal.SIGTERM)
    # elif message =="color_track":

    #     xp = 1500
    #     yp = 1500
    #     [x,y] =ct.getPos()
    #     xp=xp+x
    #     yp=yp+y
    #     xpos = str(xp)
    #     ypos = str(yp)
    #     ws.send(xpos+','+ypos+',1500,/n') 

def on_error(ws, error):
    print "### error: ###"
    print error
    main()

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### opened ###"
    global track
    xp = 1500
    yp = 1500
    px= 0.3
    py= 0.2
    dx= 0.5
    dy= 0.5
    x = 0
    y = 0
    motioncolor.init()
    start = time.time()
    while time.time()-start <= 10:
        tempx = x
        tempy = y
        [x,y] =motioncolor.getdata()
        xp=min(max(500,xp-x*px-(x-tempx)*dx),2500)
        yp=min(max(500,yp+y*py+(y-tempy)*dy),2500)
        #yp=yp-y*p
        xpos = str(int(xp))
        ypos = str(int(yp))
        ws.send(ypos+','+xpos+',1500,/n')
    #time.sleep(6)
    #track = False
    #motioncolor.kill()
    #p=Process(target=tracking, args=(ws,))
    #p.deamon = True
    #p.start()
    #p.join()

    #p.exit()

    # ws.send("rasp_sec")
    # xp = 1500
    # yp = 1500
    # px= 0.3
    # py= 0.2
    # dx= 0.5
    # dy= 0.5
    # x = 0
    # y = 0
    # motioncolor.init()
    # for i in range(0,1000):
    #     tempx = x
    #     tempy = y
    #     [x,y] =motioncolor.getdata()
    #     xp=min(max(500,xp-x*px-(x-tempx)*dx),2500)
    #     yp=min(max(500,yp+y*py+(y-tempy)*dy),2500)
    #     #yp=yp-y*p
    #     xpos = str(int(xp))
    #     ypos = str(int(yp))
    #     ws.send(ypos+','+xpos+',1500,/n') 
    #     print xpos,ypos

def main():
    time.sleep(5)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://10.0.1.35:8888/ws",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    main()
