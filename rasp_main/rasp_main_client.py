from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
#import picamera
import subprocess
import time
import serial
import os
import signal

SERVER_IP = "10.0.1.32"
uart_port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=0.2 )

class MyClient(TornadoWebSocketClient):
     def opened(self):
        print "### opened ###"
        ws.send("rasp_main")

     def received_message(self, m):
        if m.data == "start_stream":
            self.pro = subprocess.Popen(['bash', 'camerastream.sh', SERVER_IP], preexec_fn=os.setsid)
        elif m.data =="stop_stream":
            os.killpg(self.pro.pid, signal.SIGTERM)
        else:
            uart_port.write(m.data)

     def closed(self, code, reason=None):
        print "### closed ###"
     	print reason
     	ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
	
	ws = MyClient('ws://'+ SERVER_IP +':8888/ws')#, protocols=['http-only', 'chat'])
	ws.connect()
	ioloop.IOLoop.instance().start()