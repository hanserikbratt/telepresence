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
EXPECTED_CLIENTS = ("rasp_main", "rasp_sec", "oculus_client", "tracking")
cl = []
cName = {}
theTime = time.time()


class IncomingStreamHandler(TCPServer):
    """TCP server for handling incoming connections from cameras"""
    def on_chunk(self, chunk):
        cName["oculus_client"].write_message(chunk, binary=True)
    
    def on_close(self, res):
        print "res\n", res

    def handle_stream(self, stream, address):
        """Called when new IOStream object is ready for usage
        logging.info('Incoming connection from %r', address)
        PlayerConnection(stream, address, server=self)"""
        if "oculus_client" in cName:
            stream.read_until_close(self.on_close, self.on_chunk)
        else:
            raise Exception("Nowhere to send incoming video stream")
            if "rasp_sec" in cName:
                cl[cName.index("rasp_sec")].write_message("stop_stream")
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
            if "oculus_client" in cName:
                if "rasp_main" in cName:
                    cName["rasp_main"].write_message("start_stream")
                if "rasp_sec" in cName:                    
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
            if self.name == "oculus_client":
                if "rasp_main" in cName:
                    cName["rasp_main"].write_message("stop_stream")
                if "rasp_sec" in cName:
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
    tcpserver1.listen(5000)
    #tcpserver1.start(0)  # Forks multiple sub-processes
    print " Camera server Running on 5000"
    app.listen(5099)
    ioloop.IOLoop.instance().start()
