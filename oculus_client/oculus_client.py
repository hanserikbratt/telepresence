from ws4py.client.tornadoclient import TornadoWebSocketClient
import ws4py.messaging 
from tornado import ioloop
#import picamera
import subprocess
import time
import ovr
import math
import sys
import os
import ujson
from multiprocessing import Process, Queue


def oculus_tracking(queue):
    ovr.initialize(None)
    session, luid = ovr.create()
    hmdDesc = ovr.getHmdDesc(session)
    print "Servo client running"
    # Used for anti-shaking
    xtemp=0
    ytemp=0
    ztemp=0

    # Get tracking state
    ts  = ovr.getTrackingState(session, ovr.getTimeInSeconds(), True)
    if ts.StatusFlags & (ovr.Status_OrientationTracked | ovr.Status_PositionTracked):
        pose = ts.HeadPose

    # Main loop
    while True:
        ts  = ovr.getTrackingState(session, ovr.getTimeInSeconds(), True)
        if ts.StatusFlags & (ovr.Status_OrientationTracked | ovr.Status_PositionTracked):
            pose = ts.HeadPose
        
        # Get queternions
        q0 = pose.ThePose.Orientation.w;
        q1 = pose.ThePose.Orientation.x;
        q2 = pose.ThePose.Orientation.y;
        q3 = pose.ThePose.Orientation.z;

        # Calculate Euler angles
        x = int(1500 + 637*math.asin(2*(q0*q1 - q3*q2)))    #pitch
        y = int(1450 - 637*math.atan2(2*(q0*q2 - q1*q3),1-2*(q2*q2+q1*q1))) #yaw
        z = int(1500 + 637*math.asin(2*(q0*q3 + q1*q2)))    #roll

        time.sleep(0.004)
        
        # Anti-shaking
        if abs(xtemp-x)>1 or abs(ytemp-y)>1 or abs(ztemp-z)>1:
                        queue.put(str(x) + "," + str(y) + ","+str(z)+'\n')
                        sys.stdout.flush()
                        xtemp = x
                        ytemp = y
                        ztemp = z

def sendws(message):
    global ws
    ws.send(message)

class MyClient(TornadoWebSocketClient):
     def opened(self):
        global playerleft
        global playerright
        cmdlineleft = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-framedrop', '-nosound', '-']
        cmdlineright = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', 'expand=1920:960', '-geometry', '1920x960+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-framedrop', '-nosound', '-']
        self.send("oculus_client")
        #cmdline = ['mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-']
        playerleft = subprocess.Popen(cmdlineleft, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        playerright = subprocess.Popen(cmdlineright, stdin=subprocess.PIPE)
        print "### opened ###"
    	#self.close(reason="Close because end of loop")

     def received_message(self, m):
        global playerleft
        global playerright
        global queue
        global leftEye
        if isinstance(m,ws4py.messaging.BinaryMessage):
            if leftEye:
                playerleft.stdin.write(m.data)
            else:
                playerright.stdin.write(m.data)
        else:
            leftEye = m.data == "rasp_sec"

        if not queue.empty():
            self.send(queue.get())

     def closed(self, code, reason=None):
        print "### closed ###"
     	print reason
     	ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    global ws
    ws = MyClient('ws://telepresence.precisit.com:5099/ws')
    global queue
    queue = Queue()
    tracking_process = Process(target=oculus_tracking, args=(queue,))
    tracking_process.start()
    #tracking_process.join()
    ws.connect()
    ioloop.IOLoop.instance().start()