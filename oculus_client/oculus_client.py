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


class OculusTracker(object):
    """docstring for OculusTracker"""
    def __init__(self):
        ovr.initialize(None)
        self.session, luid = ovr.create()
        hmdDesc = ovr.getHmdDesc(self.session)
        print "Servo client running"
        # Used for anti-shaking
        self.xtemp=0
        self.ytemp=0
        self.ztemp=0
        
    def get_pos_command(self):
        ts  = ovr.getTrackingState(self.session, ovr.getTimeInSeconds(), True)
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
        
        pos_command = ""
        # Anti-shaking
        if abs(self.xtemp-x)>1 or abs(self.ytemp-y)>1 or abs(self.ztemp-z)>1:
            pos_command = (str(x) + "," + str(y) + ","+str(z)+'\n')
            sys.stdout.flush()
            self.xtemp = x
            self.ytemp = y
            self.ztemp = z
        return pos_command


class MyClient(TornadoWebSocketClient):
     def opened(self):
        global player
        self.oculusTracker = OculusTracker()
        cmdlineleft = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+960+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-framedrop', '-nosound', '-']
        self.send("oculus_client_main")
        player = subprocess.Popen(cmdlineleft, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        print "### opened ###"

     def received_message(self, m):
        global player
        global queue
        if isinstance(m,ws4py.messaging.BinaryMessage):
            player.stdin.write(m.data)

        pos_command = self.oculusTracker.get_pos_command()
        if pos_command:
            self.send(pos_command)

     def closed(self, code, reason=None):
        print "### closed because: ###"
     	print reason
     	ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    global ws
    ws = MyClient('ws://telepresence.precisit.com:5099/ws')
    ws.connect()
    ioloop.IOLoop.instance().start()