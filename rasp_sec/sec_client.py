import websocket
import time
import subprocess
import signal
import os
import re
import motioncolor


#Websocket client connecting to the local server and handling
#the starting of the camera stream and colortracking
#on the secondary raspberry pi .


def on_message(ws, message):
    global pro
    print message

# Starting camera stream by running a subprocess with
# the shell script camerastream.sh
    if message[0:13] == "start_stream:":
        ip = re.search("start_stream:(.+?)#", message).group(1)
        pro = subprocess.Popen(['bash', 'camerastream.sh', ip],\
            preexec_fn=os.setsid)

# Beta implementation of colortracking (running the colortracking 20 seconds)
    elif message == "start_tracking":
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
        while time.time()-start <= 20:
            tempx = x
            tempy = y
            [x,y] =motioncolor.getdata()
            xp=min(max(500,xp-x*px-(x-tempx)*dx),2500)
            yp=min(max(500,yp+y*py+(y-tempy)*dy),2500)
            xpos = str(int(xp))
            ypos = str(int(yp))
            ws.send(ypos+','+xpos+',1500,/n')
        motioncolor.kill()

# Stoping camera stream subprocess
    elif message =="stop_stream":
            os.killpg(pro.pid, signal.SIGTERM)

def on_error(ws, error):
    print "### error: ###"
    print error
    main()              # on error keep trying to establish connection

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### opened ###"
    ws.send("rasp_sec")

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
