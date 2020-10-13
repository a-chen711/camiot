import socket
import time

c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(('192.168.1.108',8011))


while True:
	data=c.recv()
	print(data)
	time.sleep(2)