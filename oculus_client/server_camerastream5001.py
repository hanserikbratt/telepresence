import socket
import subprocess
#from win32api import GetSystemMetrics

#screenWidth = GetSystemMetrics(0)
#screenHeight = GetSystemMetrics(1)

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 5001))
server_socket.listen(0)
print " Camera server Running on 5001"
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    # Run mplayer as a windows cmdline
    #cmdline = ['mplayer-svn-37552\mplayer', '-geometry', '1024x768+-12+168', '-fps', '75', '-cache', '1024', '-x', '1296', '-y', '972', '-vo', 'gl', '-framedrop', '-nosound', '-']
    #cmdline = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-']
    cmdline = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', 'expand=1200:::::8/9', '-geometry', '960x1200+0+64', '-fps', '75', '-cache', '1024', '-vo', 'gl', '-framedrop', '-nosound', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Reading 1k of data from the socket connetion and write it to
        # mplayer's stdin
        data = connection.read(1024)
        if not data:
             break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()
    player.terminate()
