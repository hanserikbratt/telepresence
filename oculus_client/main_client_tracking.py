# import the necessary packages
import websocket
import time
import subprocess
import sys
print "Servo client running"

def on_message(ws, message):
    print message

def on_error(ws, error):
    print "### error: ###"
    print error

def on_close(ws):
    print "### closed ###"
    ovr.destroy(session)
    ovr.shutdown()

def on_open(ws):
    print "### opened ###"
    ws.send("tracking")

    for i in range(0,1000000):
    	x = 0
    	time.sleep(0.004)

    ws.close()

if __name__ == "__main__":
    ip = str(sys.argv[1])
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://"+ip+":8888/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
