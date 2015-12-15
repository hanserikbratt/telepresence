# telepresence
Source code for the telepresence project

## PC

The setup is tested on a computer running Windows (tested on Windows 7 and 8.1) and requires a full HD screen. We recommend an Intel Core i5 or equivalently and a nVidia GTX 750 Ti or higher.

Softwares needed:

* **Virtual desktop** (http://www.vrdesktop.net)
* **Oculus Rift runtime SDK 0.8.0.0** (https://developer.oculus.com/downloads/)
* **MPlayer** (http://sourceforge.net/projects/mplayerwin/)
* **Python 2.7** (https://www.python.org/downloads/windows/)

MPlayer needs to be installed in the oculus_client folder with the name **mplayer-svn-37552**, otherwise the scripts will not be able to use it.

Python dependencies:

* **ovr** *(0.8.3rc0)*
* **tornado** *(4.3)*
* **websocket-client** *(0.34.0)*
* **ws4py** *(0.3.4)*

To install these Python librarys uses '''pip install''' followed by the library name

## Other
The gimbal requires an outlet and two eternet ports. The Oculus Rift requires one outlet.

To program the MCU running the Arduino Bootloader a Arduino Breadboard is required. Follow [this](https://www.arduino.cc/en/Tutorial/ArduinoToBreadboard) for a tutorial on how to do this. 