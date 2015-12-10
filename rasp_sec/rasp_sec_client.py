# Websocket client handeling the starting of the camera stream and colortracking
# on the secondary raspberry pi 2.

# import the necessary packages
from tornado import ioloop
from ws4py.client.tornadoclient import TornadoWebSocketClient
import time
import subprocess
import signal
import os
import motioncolor

SERVER_IP = "telepresence.precisit.com"

class MyClient(TornadoWebSocketClient):

    def opened(self):
        print "### opened ###"
        self.send("rasp_sec")

    def received_message(self, m):
        print m.data

    # Starting camera stream by running a subprocess with the shell script camerastream.sh
        if m.data == "start_stream":
                self.pro = subprocess.Popen(['bash', 'camerastream.sh', SERVER_IP], preexec_fn=os.setsid)

    # Beta implementation of colortracking (running the colortracking 20 seconds)
        elif m.data == "start_tracking":
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

    # Stopping camera stream subprocess
        elif m.data =="stop_stream":
                os.killpg(self.pro.pid, signal.SIGTERM)

    def closed(self, code, reason=None):
        print "### closed ###"
        print reason
        ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    ws = MyClient('ws://'+ SERVER_IP +':5099/ws')
    ws.connect()
    ioloop.IOLoop.instance().start()
