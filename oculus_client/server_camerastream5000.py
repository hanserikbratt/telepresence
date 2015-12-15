import socket
import subprocess

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(0)
print " Camera server Running on 5000"
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    
    # Run mplayer as a windows cmdline
    cmdline = ['mplayer-svn-37552\mplayer', '-noborder', '-vf', \
    'expand=1920:960', '-geometry', '1920x960+0+64', '-fps', '75', \
    '-cache', '1024', '-vo', 'gl', '-framedrop', '-nosound', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(1024)
        if not data:
             break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()
    player.kill()
