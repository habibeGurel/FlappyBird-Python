import socket

sock = socket.socket()

host = "172.20.10.13" #ESP32 IP in local network
port = 80             #ESP32 Server Port

sock.connect((host, port))
sock.send("test")
sock.close()
