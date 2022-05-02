import socket

HOST = '127.0.0.1'
PORT = 65432
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))

while True:
    msg = conn.recv(1024)
    print(msg.decode())
    msg2 = input()
    conn.send(msg2.encode())


conn.close()