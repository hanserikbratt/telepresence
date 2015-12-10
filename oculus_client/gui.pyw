# import the necessary packages
from Tkinter import *
import subprocess
import time

root = Tk()

# Get screen resolution
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
# default IP
ipmain = "10.0.1.35" 
# Set top bar attributes
background_image=PhotoImage(file= "~/Dropbox/Projekt_inbyggda/precisit2.gif")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
root.title("Telepresence")
root.tk_setPalette(background='#FFFFFF')
root.geometry('%dx%d+%d+%d' % (screenWidth, 64, 0, 0))
root.overrideredirect(1)                                                        # Removing borders
root.lift()
root.wm_attributes("-topmost", True)

# Set background window
background = Tk()
background.geometry('%dx%d+%d+%d' % (screenWidth, screenHeight, 0, 64))
background.overrideredirect(1)                                                      # Removing borders
background.tk_setPalette(background='#000000')

#Uncomment to insert HUD

# Set HUD attributes
#hudText = "HUD"

#leftHUD = Tk()
#leftHUD.geometry('%dx%d+%d+%d' % (200, 100, 400, 500))
#leftHUD.overrideredirect(1)                                                      # Removing borders
#leftHUD.lift()
#leftHUD.wm_attributes("-topmost", True)
#leftHUD.attributes("-alpha", 1)                                                # Making the HUD windown transparent 

#lefttext = Text(leftHUD, height=2, width=30, font = ('Comic Sans', 30, 'bold'))
#lefttext.pack()
#lefttext.insert(END, hudText)

#rightHUD = Tk()
#rightHUD.geometry('%dx%d+%d+%d' % (200, 100, 1300, 500))
#rightHUD.overrideredirect(1)                                                      # Removing borders
#rightHUD.lift()
#rightHUD.wm_attributes("-topmost", True)
#rightHUD.attributes("-alpha", 1)                                                # Making the HUD windown transparent 

#righttext = Text(rightHUD, height=2, width=30, font = ('Comic Sans', 30, 'bold'))
#righttext.pack()
#righttext.insert(END, hudText)

# Set bottom bar attributes
bottom = Tk()
bottom.tk_setPalette(background='#FFFFFF')
bottom.geometry('%dx%d+%d+%d' % (screenWidth, 56, 0, screenHeight - 56))
bottom.overrideredirect(1)                                                      # Removing borders
bottom.lift()
bottom.wm_attributes("-topmost", True)

# Run mode
def runLocal():
        global mainproc, subproc1, subproc2
        # Setting button states.
        stereobuttonlocal['state']=DISABLED
        stereobuttonglobal['state']=DISABLED
        trackingbutton['state']=DISABLED
        endbutton['state']=NORMAL

        mainproc = subprocess.Popen('python main_client.py '+ip.get())
        subproc1 = subprocess.Popen('python server_camerastreamD5000.py')
        subproc2 = subprocess.Popen('python server_camerastream5001.py') 
        
        #time.sleep(10)                                                          # HUD alive time
        #leftHUD.destroy()
        #rightHUD.destroy()
        

 # Run mode
def runGlobal():
        global subproc1, subproc2
        # Setting button states.
        stereobuttonlocal['state']=DISABLED
        stereobuttonglobal['state']=DISABLED
        trackingbutton['state']=DISABLED
        endbutton['state']=NORMAL

        subproc1 = subprocess.Popen('python oculus_client.py')
        subproc2 = subprocess.Popen('python oculus_client2.py')

        
        #time.sleep(10)                                                          # HUD alive time
        #leftHUD.destroy()
        #rightHUD.destroy()
               
# Tracking mode
def tracking():
        global mainproc, subproc1
        stereobuttonlocal['state']=DISABLED
        stereobuttonglobal['state']=DISABLED
        trackingbutton['state']=DISABLED
        endbutton['state'] = DISABLED
        quitbutton['state'] = DISABLED
        mainproc = subprocess.Popen('python main_client_tracking.py '+ip.get())
        subproc1 = subprocess.Popen('python server_camerastream5000.py')
        time.sleep(20)
        endbutton['state'] = NORMAL
        quitbutton['state'] = NORMAL
        end()

# End current video stream
def end():
        stereobuttonlocal['state']=NORMAL
        stereobuttonglobal['state']=NORMAL
        trackingbutton['state']=NORMAL
        endbutton['state']=DISABLED

        try:
                mainproc.kill()
        finally:
                subproc1.kill()
                subproc2.kill()
                                
# End video and also close GUI           
def endgui():
        try:
                try:        
                        mainproc.kill()
                finally:
                        subproc1.kill()
                        subproc2.kill()
        except:
                None
        finally:
                root.destroy()
                background.destroy()
                bottom.destroy()

                #HUD windows
                #leftHUD.destroy()
                #rightHUD.destroy()

# Place buttons
stereobuttonlocal = Button(root, highlightthickness=0, text="Run local", fg="black", command = runLocal)
stereobuttonlocal.place(x=100, y=18)

trackingbutton = Button(root, highlightthickness=0, text="Track local", fg="black", command = tracking)
trackingbutton.place(x=300, y=18)

endbutton = Button(root, highlightthickness=0, text="End", state=DISABLED, fg="black", command = end)
endbutton.place(x=400, y=18)

quitbutton = Button(root, highlightthickness=0, text="Quit GUI", fg="black", command = endgui)
quitbutton.place(x=1800, y=18)

stereobuttonglobal = Button(root, highlightthickness=0, text="Run global", fg="black", command = runGlobal)
stereobuttonglobal.place(x=200, y=18)


# Place IP entry field
iplabel = Label(root, text="IP to main RPI")
iplabel.place(x= 550,y=22)

ip = Entry(root)
ip.insert(10, ipmain)
ip.place(x=650,y=24)

# Start root
root.mainloop()
