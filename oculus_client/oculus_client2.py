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


class MyClient(TornadoWebSocketClient):
     def opened(self):
        global player
        #global playerright
        cmdlineleft = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-framedrop', '-nosound', '-']
        #cmdlineright = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', 'expand=1920:960', '-geometry', '1920x960+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-framedrop', '-nosound', '-']
        self.send("oculus_client_sec")
        #cmdline = ['mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-']
        player = subprocess.Popen(cmdlineleft, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        #playerright = subprocess.Popen(cmdlineright, stdin=subprocess.PIPE)
        print "### opened ###"
    	#self.close(reason="Close because end of loop")

     def received_message(self, m):
        global player
        #global playerright
        if isinstance(m,ws4py.messaging.BinaryMessage):
            player.stdin.write(m.data)

     def closed(self, code, reason=None):
        print "### closed ###"
     	print reason
     	ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    global ws
    ws = MyClient('ws://telepresence.precisit.com:5099/ws')
    ws.connect()
    ioloop.IOLoop.instance().start()