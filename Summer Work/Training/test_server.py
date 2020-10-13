import socket

# ------------------------------------------ #
#           Server Client Interface          #
# ------------------------------------------ #
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
HOST = '192.168.1.118'
PORT = 8200

print('done')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print('Server has received ' + str(data) + ' from the client')
            if not data:
                break
            conn.sendall(b'Yeet')

