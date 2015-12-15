# telepresence
Source code for the telepresence project. The aim of the project was to control a camera gimbal using the Oculus Rift DK2 

##Raspberry pi setup
For setting up one Raspberry Pi you need at least these things:

* A Raspberry pi. (We have been using the Raspberry pi 2)
* A 8 GB microSD card 
* Some way of writing to the SD card
* A router with one ethernet port available
* An ethernet cable
* A 5v DC power supply

Download the [latest version]( http://downloads.raspberrypi.org/raspbian_latest) of the operating system Raspbian. (we used 2015-11-21-raspbian-jessie).

follow [this](https://www.raspberrypi.org/documentation/installation/installing-images/) guide on how to install a OS to an SD card.

Insert the SD card into your Raspberry Pi, connect an Ethernet cable and power it up by connecting the power supply.

In this guide we will only connect to the Raspberry Pi by SSH, so if you are using Windows you will need a SSH-client, such as [putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).

Find out the ip of the RPi by following [this](https://www.raspberrypi.org/documentation/troubleshooting/hardware/networking/ip-address.md) guide. 

SSH into your RPi by the steps described in [this](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md) guide.

When you have succesfully accessed the command line on your RPi it is a good idea to configure the Raspberry Pi by running the command `raspi-config`.

In the configuration screen choose Expand filesystem to ensure that the RPi will use all of the available disk space on you SD-card.

Once you have rebooted after the filesystem expansion it can be a good idea to run `apt-get update` and `apt-get upgrade` to make sure the RPi has the latest updates.

###Camera and streaming

After this is done access the configuration screen again by typing `raspi-config` 

This time navigate to `Enable Camera`, select `Enable`, `Finish` and `Yes` to reboot

Now you might want to check if the camera is working. The command ` raspistill -o testImage.jpg` takes a picture with the camera and it will be listed in the current folder. 

Now we want to get the source code for this project. The code in the `rasp_main` folder goes in the main RPi, and the the code in the folder`rasp_sec` goes in the secondary RPi. 

To be able to stream video, the tool `netcat` will be used. Install this by the commmand `sudo apt-get install netcat-traditional`. 

The RPi video will be captured into a FIFO buffer. To create a FIFO buffer use the command `mkfifo fifo.500`. Make sure that the buffer file is in the same folder as the source code. For more information about the streaming process, see [this](http://zacharybears.com/low-latency-raspberry-pi-video-streaming/)





## Server
The server script **global_server** is tested on a [Amazon EC2 debian server](https://aws.amazon.com/ec2). To run the script the following is required.

Softwares needed:

* **Python 2.7**
* **pip 7.1.2** (https://pypi.python.org/pypi/pip)

On a debian server these softwares can be installed using the `sudo apt-get` command followed by the name.

Python dependencies:

* **tornado** *(4.3)*

To install this Python library uses the `pip install` command followed by the library name.

The following ports need to be open:

* 5000
* 5001
* 5099 

## PC

The setup is tested on a computer running Windows (tested on Windows 7 and 8.1) and requires a full HD screen. We recommend an Intel Core i5 or equivalently and a nVidia GTX 750 Ti or higher.

Softwares needed:

* **Virtual desktop** (http://www.vrdesktop.net)
* **Oculus Rift runtime SDK 0.8.0.0** (https://developer.oculus.com/downloads/)
* **MPlayer** (http://sourceforge.net/projects/mplayerwin/)
* **Python 2.7** (https://www.python.org/downloads/windows/)
* **pip 7.1.2** (https://pypi.python.org/pypi/pip)

Virtual desktop is uesd to mirror the desktop to the Oculus Rift DK2. The setup is calibrated to use the side-by-side mirroring with distortion (F9 mode).
MPlayer needs to be installed in the **oculus_client** folder with the name **mplayer-svn-37552**, otherwise the scripts will not be able to use it.

Python dependencies:

* **ovr** *(0.8.3rc0)*
* **tornado** *(4.3)*
* **websocket-client** *(0.34.0)*
* **ws4py** *(0.3.4)*

To install these Python librarys uses the `pip install` command followed by the library name.

## Other
The gimbal requires an outlet and two ethernet ports. The Oculus Rift requires one outlet.

To program the MCU running the Arduino Bootloader a Arduino Breadboard is required. Follow [this](https://www.arduino.cc/en/Tutorial/ArduinoToBreadboard) for a tutorial on how to do this.

Running the local implementation requires:

* The PC and the gimbal to be connected to the same network
* The networks router to have port 22, 5000 and 5001 open
* Need to know the main Raspbarry Pi´s IP address
* mer? 
