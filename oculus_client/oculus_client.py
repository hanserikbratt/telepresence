from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
#import picamera
import subprocess
import time

class MyClient(TornadoWebSocketClient):
     def opened(self):
        #cmdline = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+0+64', '-fps', '75', '-cache', '2048', '-vo', 'gl', '-framedrop', '-nosound', '-']
        global player
        self.send("oculus_client")
        cmdline = ['mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        print "### opened ###"
    	#self.close(reason="Close because end of loop")

     def received_message(self, m):
        global player
        player.stdin.write(m.data)

     def closed(self, code, reason=None):
        global player
        print "### closed ###"
     	print reason
     	ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
	
	ws = MyClient('ws://10.0.1.32:8888/ws')#, protocols=['http-only', 'chat'])
	ws.connect()
	ioloop.IOLoop.instance().start()