from tornado import websocket, web, ioloop
from tornado.tcpserver import TCPServer
import math
import sys
import time
import subprocess
import os
import signal

"""
this script acts as a websocket-server, checking which client is connecting and sending commands on whether to 
stream or not. It also acts as two TCP servers, relaying the stream to appropriate websocket.
"""


EXPECTED_CLIENTS = ("rasp_main", "rasp_sec", "oculus_client_main","oculus_client_sec", "tracking_client")
cl = []     #list of connected clients.
cName = {}  #dictionary of connected clients names.

class IncomingStreamHandler(TCPServer):
    """
    TCP server for handling incoming connections from cameras. 
    extends the tornado TCPServer
    """

    def set_clients(self, camName, wsName):
        """ sets the names of incoming stream and outgoing stream
        Attributes:
        camName: name of incoming camera streamer i.e "rasp_main" or "rasp_sec"
        wsName: name of recieving websocket. i.e "oculus_client_main" or "oculus_client_sec"
        """
        self.camName = camName
        self.wsName = wsName

    def on_chunk(self, chunk):
        """defines what is to be done on incoming chunk of data"""
        cName[self.wsName].write_message(chunk, binary=True)
    
    def on_close(self, res):
        print "res\n", res

    def handle_stream(self, stream, address):
        """Called when new IOStream object is ready for usage"""
        if self.wsName in cName:
            stream.read_until_close(self.on_close, self.on_chunk)
        else:
            raise Exception("Nowhere to send incoming video stream")
            cName[self.camName].write_message("stop_stream")
            stream.close()

class SocketHandler(websocket.WebSocketHandler):
    """Class for handling the websocket connections."""
    def check_origin(self, origin):
        return True

    def open(self):
        self.name = ""
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        """Method that is called when recieving message.
        all clients is expected to send their name when first connected"""
        if message in EXPECTED_CLIENTS:
            self.name = message
            cName[message] = self
            print "### connected to " +  message + " ###"
            if (self.name == "oculus_client_main" and "rasp_main" in cName) or (self.name == "rasp_main" and "oculus_client_main" in cName):
                cName["rasp_main"].write_message("start_stream")
            if (self.name == "oculus_client_sec" and "rasp_sec" in cName) or (self.name == "rasp_sec" and "oculus_client_sec" in cName):
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
        """Method called upon closed connection."""
        if self.name in EXPECTED_CLIENTS:
            print self.name
            if self.name=="oculus_client_main" and "rasp_main" in cName:
                cName["rasp_main"].write_message("stop_stream")
            if self.name == "oculus_client_sec" and "rasp_sec" in cName:
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
    """On execution this script starts two TCP servers on port 5000 and 5001.
        It then starts the websocket server."""
    tcpserver1 = IncomingStreamHandler()
    tcpserver1.set_clients("rasp_main", "oculus_client_main")
    tcpserver1.listen(5000)
    print " Camera server Running on 5000"
    tcpserver2 = IncomingStreamHandler()
    tcpserver2.set_clients("rasp_sec", "oculus_client_sec")
    tcpserver2.listen(5001)
    print " Camera server Running on 5001"
    app.listen(5099)
    ioloop.IOLoop.instance().start()
