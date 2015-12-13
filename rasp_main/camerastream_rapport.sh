cat fifo.500 | nc.traditional $1 5000 &
/opt/vc/bin/raspivid -w 1296 -h 972 -fps 42 \
-rot 180 -n -o fifo.500 -t 0 -b 10000000 &

