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

follow [this](https://www.raspberrypi.org/documentation/installation/installing-images/) guide on how to install an OS to a SD card.

Insert the SD card into your Raspberry Pi, connect an Ethernet cable and power it up by connecting the power supply.

In this guide we will only connect to the Raspberry Pi by SSH, so if you are using Windows you will need a SSH-client, such as [putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).

Find out the ip of the RPi by following [this](https://www.raspberrypi.org/documentation/troubleshooting/hardware/networking/ip-address.md) guide. 

SSH into your RPi by the steps described in [this](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md) guide.

When you have succesfully accessed the command line on your RPi it is a good idea to configure the Raspberry Pi by running the command `raspi-config`.

In the configuration screen choose Expand filesystem to ensure that the RPi will use all of the available disk space on your SD-card.

Once you have rebooted after the filesystem expansion it can be a good idea to run `apt-get update` and `apt-get upgrade` to make sure the RPi has the latest updates.

For setting up another RPi, repeat the process.

####Setting up for the Source code

After the setup is done access the configuration screen again by typing `raspi-config`.

This time navigate to `Enable Camera`, select `Enable`, `Finish` and `Yes` to reboot

Now you might want to check if the camera is working. The command ` raspistill -o testImage.jpg` takes a picture with the camera and it will be listed in the current folder. 

Now we want to get the source code for this project. The code in the **rasp_main** folder goes in the main RPi, and the the code in the folder **rasp_sec** goes in the secondary RPi. The easiest way to do this is to use git by typing `git clone https://github.com/precisit/telepresence`

The RPi video will be captured into a FIFO buffer. To create a FIFO buffer use the command `mkfifo fifo.500`. Make sure that the buffer file is in the same folder as the source code. For more information about the streaming process, see [this](http://zacharybears.com/low-latency-raspberry-pi-video-streaming/).

To make the RPi communicate with the MCU one needs to [turn off the UART pins functioning as a serial console](http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/io-pins-raspbian/uart-pins)

Now we are ready to install dependencies. The Linux tools needed are 

* netcat-traditional
* python-pip
* python-serial

install these by typing `sudo apt-get install package-name`

We also need to install some python packages. These are:

* ws4py
* websocket-client
* tornado

use the `pip-install` command to install these.

Additional packages are also needed if one wants to implement the colortracking feature. These are described below. If you want to skip the colortracking feature, **comment out the motioncolor import** in **sec_client.py** and **glocal_sec_client.py**.

We also  need to change the IP in some of the scripts. In **global_main_client.py** and **global_sec_client.py** change the server IP to your global server if you are using one. In **sec_client.py** change the server IP to your main RPi IP.

## Server
The server script **global_server** is tested on a [Amazon EC2 debian server](https://aws.amazon.com/ec2). If you don't want to run the setup globally the following is not required.

Software needed:

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

To start the server, make sure the script **global_server.py** is located on the server, and run `python global_server.py &`
#### Color tracking


## PC

The setup is tested on a computer running Windows (tested on Windows 7 and 8.1) and requires a full HD screen. We recommend an Intel Core i5 or equivalently and a nVidia GTX 750 Ti or higher.

Software needed:

* **Virtual desktop** (http://www.vrdesktop.net)
* **Oculus Rift runtime SDK 0.8.0.0** (https://developer.oculus.com/downloads/)
* **MPlayer** (http://sourceforge.net/projects/mplayerwin/)
* **Python 2.7** (https://www.python.org/downloads/windows/)
* **pip 7.1.2** (https://pypi.python.org/pypi/pip)

Virtual desktop is used to mirror the desktop to the Oculus Rift DK2. The setup is calibrated to use the side-by-side mirroring with distortion (F9 mode).

MPlayer needs to be installed in the **oculus_client** folder with the name **mplayer-svn-37552**, otherwise the scripts will not be able to use it.

Python dependencies:

* **ovr** *(0.8.3rc0)*
* **tornado** *(4.3)*
* **websocket-client** *(0.34.0)*
* **ws4py** *(0.3.4)*

To install these Python librarys uses the `pip install` command followed by the library name.

## Other
The gimbal requires an outlet and two ethernet ports. The Oculus Rift requires one outlet.

To program the MCU running the Arduino Bootloader an Arduino Breadboard is required. Follow [this](https://www.arduino.cc/en/Tutorial/ArduinoToBreadboard) for a tutorial on how to do this.

Running the local implementation requires:

* The PC and the gimbal to be connected to the same network
* Need to know the main Raspbarry Pi´s IP address
* mer? 

## Deployment

SSH into the main RPi

run the script **global_main_client.py** if you want a global setup and/or *main_server.py* if you want the local setup.

SSH into the secondary RPi

run the script **global_sec_client.py** if you want a global setup and/or **sec_client.py** if you want the local setup.

SSH into the global server if you want the global setup and start the script **global_server-py**. 

The global scripts will take some time to connect to the server

run **gui.pyw** on your windows computer connected to the oculus rift.

choose to connect globally or locally, if you choose locally you must also iput the main RPi IP.

If you dont want to start the RPi scripts manually in the future you can use the linux tool Crontab and add a line starting the global and/or local scripts at startup. To do this SSH into the RPi and type `crontab -e` and press enter. Add a line like the following:

`@reboot python /home/pi/main_server.py & python /home/pi/global_main_client.py &`
