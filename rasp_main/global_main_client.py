from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
import subprocess
import time
import serial
import os
import signal


#This client handles the websocket connection to the global server
#from the main raspberry pi. 
#In more detail it listen for commands to stop and start the camerastream 
#and relays messages concerning orientation to the MCU


SERVER_IP = "telepresence.precisit.com"
uart_port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=0.2 )

class MyClient(TornadoWebSocketClient):
     def opened(self):
        print "### opened ###"
        self.send("rasp_main")

     def received_message(self, m):
        print m.data
        if m.data == "start_stream":
            self.pro = subprocess.Popen(['bash',\
                'camerastream.sh', SERVER_IP], preexec_fn=os.setsid)
        elif m.data =="stop_stream":
            os.killpg(self.pro.pid, signal.SIGTERM)
        else:
            uart_port.write(m.data)

     def closed(self, code, reason=None):
        print "### closed ###"
     	print reason
        ioloop.IOLoop.instance().stop()

def main():
	time.sleep(20)
	ws = MyClient('ws://'+ SERVER_IP +':5099/ws')
	ws.connect()
	ioloop.IOLoop.instance().start()    		

if __name__ == '__main__':
	main()