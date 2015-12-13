from tornado import websocket, web, ioloop
import math
import sys
import time
import subprocess
import serial
import os
import signal

#The local server for handling camera streaming and sending the 
#data coming from the Oculus rift to the MCU via uart.


uart_port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=0.2 )

cl = []
cName = []
mainIP =""
class SocketHandler(websocket.WebSocketHandler):
    #main class for handling the websocket connections.
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        #Method that is called when recieving message.
        #all clients is expected to send their name when first connected
        global mainIP
        print mainIP
        print message
        if message=="rasp_sec":
            cName.insert(cl.index(self), "rasp_sec")
            print "### connected to rasp_sec ###"
            if "main_client" in cName:
                self.write_message("start_stream:" + mainIP + "#")
            elif "tracking" in cName:
                self.write_message("start_tracking")   
        elif message=="main_client":
            cName.insert(cl.index(self), "main_client")
            mainIP = str(self.request.remote_ip)
            print "### connected to main_client ###"
            
            #starts the camera streaming on the local camera.
            #Attaches a session id which is later used for killing 
            #the session, including its subprocess, on closing of the websocket.
            self.pro = subprocess.Popen(['bash', 'camerastream.sh', mainIP],\
                preexec_fn=os.setsid)
            
            if "rasp_sec" in cName:
                cl[cName.index("rasp_sec")].write_message("start_stream:"\
                 + mainIP + "#")
        elif message=="tracking":
            cName.insert(cl.index(self), "tracking")
            mainIP = str(self.request.remote_ip)
            print "### connected to tracking client ###"
            self.pro = subprocess.Popen(['bash', 'camerastream.sh', mainIP],\
                preexec_fn=os.setsid)
            if "rasp_sec" in cName:
                cl[cName.index("rasp_sec")].write_message("start_tracking")

        else:
            uart_port.write(message)

    def on_close(self):
        print "### closing to " + cName[cl.index(self)] +  " ###"
        os.killpg(self.pro.pid, signal.SIGTERM)
        if "rasp_sec" in cName:
            cl[cName.index("rasp_sec")].write_message("stop_stream")
        
        if self in cl:
            cName.pop(cl.index(self))
            cl.remove(self)

app = web.Application([
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
