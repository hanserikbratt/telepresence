from tornado import websocket, web, ioloop
from tornado.tcpserver import TCPServer
import math
import sys
import time
import subprocess
#import serial
import os
import signal
#import socket

SERVER_IP = "10.0.1.32"
EXPECTED_CLIENTS = ("rasp_main", "rasp_sec", "oculus_client_main","oculus_client_sec", "tracking")
cl = []
cName = {}
theTime = time.time()


class IncomingStreamHandler(TCPServer):
    """TCP server for handling incoming connections from cameras"""

    def set_clients(self, camName):
        self.camName = camName
        self.wsName = wsName

    def on_chunk(self, chunk):, wsName
        cName[self.wsName].write_message(chunk, binary=True)
    
    def on_close(self, res):
        print "res\n", res

    def handle_stream(self, stream, address):
        """Called when new IOStream object is ready for usage
        logging.info('Incoming connection from %r', address)
        PlayerConnection(stream, address, server=self)"""
        if self.wsName in cName:
            stream.read_until_close(self.on_close, self.on_chunk)
        else:
            raise Exception("Nowhere to send incoming video stream")
            cName[self.camName].write_message("stop_stream")
            stream.close()

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
    	#global player
        self.name = ""
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        if message in EXPECTED_CLIENTS:
            self.name = message
            cName[message] = self
            print "### connected to " +  message + " ###"
            if "oculus_client_main" in cName and "rasp_main" in cName:
                cName["rasp_main"].write_message("start_stream")
            if "oculus_client_sec" in cName and "rasp_sec" in cName:
                cName["rasp_sec"].write_message("start_stream")
            elif "tracking_client" in cName:
                if "rasp_main" in cName:
                    cName["rasp_main"].write_message("start_stream")
                if "rasp_sec" in cName:                    
                    cName["rasp_sec"].write_message("start_tracking")
        elif "rasp_main" in cName:
            cName["rasp_main"].write_message(message)
        else:
            print message
        

    def on_close(self):
        if self.name in EXPECTED_CLIENTS:
            if "oculus_client_main" in cName and "rasp_main" in cName:
                cName["rasp_main"].write_message("stop_stream")
            if "oculus_client_sec" in cName and "rasp_sec" in cName:
                cName["rasp_sec"].write_message("stop_stream")
            del cName[self.name]
            print "### closing to " + self.name +  " ###"
        else:
            print "### closing to unexpected client ###"
        cl.remove(self)

app = web.Application([
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    tcpserver1 = IncomingStreamHandler()
    tcpserver1.set_clients("rasp_main")
    tcpserver1.listen(5000)
    print " Camera server Running on 5000"
    tcpserver2 = IncomingStreamHandler()
    tcpserver2.set_clients("rasp_sec")
    tcpserver2.listen(5001)
    print " Camera server Running on 5001"
    #tcpserver1.start(0)  # Forks multiple sub-processes
    app.listen(5099)
    ioloop.IOLoop.instance().start()
