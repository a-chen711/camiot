import socket
import time
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('Socket created')
s.bind(('192.168.1.108',8011))
s.listen(10)
print ('Socket now listening')
# Accpet the client 
conn,addr=s.accept()

while True:
	conn.sendall(b'True')
	time.sleep(1)

