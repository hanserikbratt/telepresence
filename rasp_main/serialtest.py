import serial
import time
import sys

uart_port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1.0 )

def main():
	try:
		p=str(sys.argv[1])
		y=str(sys.argv[2])
		r=str(sys.argv[3])
	except IndexError:
		p="1000"
		y="1000"
		r="1000"
	out = ""
	uart_port.write(p + "," + y + "," + r + '\n')
	time.sleep(1)
	while uart_port.inWaiting()>0:
		out += uart_port.read(1)
	print out

if __name__ == '__main__':
	main()