# import the necessary packages
import websocket
import time
import subprocess
import ovr
import sys
import math
ovr.initialize(None)
session, luid = ovr.create()
hmdDesc = ovr.getHmdDesc(session)
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
    ws.send("main_client")

    # Used for anti-shaking
    xtemp=0
    ytemp=0
    ztemp=0

    # Main loop
    while True:
        ts  = ovr.getTrackingState(session, ovr.getTimeInSeconds(), \
            True)
        if ts.StatusFlags & (ovr.Status_OrientationTracked | \
            ovr.Status_PositionTracked):
            pose = ts.HeadPose
        
        # Get queternions
        q0 = pose.ThePose.Orientation.w;
        q1 = pose.ThePose.Orientation.x;
        q2 = pose.ThePose.Orientation.y;
        q3 = pose.ThePose.Orientation.z;

        # Calculate Euler angles
        x = int(1500 + 637*math.asin(2*(q0*q1 - q3*q2)))    #pitch
        y = int(1450 - 637*math.atan2(2*(q0*q2 - q1*q3),1 \
        - 2*(q2*q2 + q1*q1))) #yaw
        z = int(1500 + 637*math.asin(2*(q0*q3 + q1*q2)))    #roll

        time.sleep(0.004)
		
		# Anti-shaking
        if abs(xtemp-x)>1 or abs(ytemp-y)>1 or abs(ztemp-z)>1:
                        ws.send(str(x) + "," + str(y) + "," \
                            + str(z) + '\n')
                        sys.stdout.flush()
                        xtemp = x
                        ytemp = y
                        ztemp = z
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
