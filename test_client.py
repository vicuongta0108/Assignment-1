import socket
import sys

USERNAME = sys.argv[1]
HOST = sys.argv[2]
PORT = sys.argv[3]

# Create a client socket to connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send message as fast as possible
while True:
    message = 'Pew! Pew! Pew!'
    client_socket.send(message.encode())
    data = client_socket.recv(1024).decode()
    if data == 'quit':
        break
    
client_socket.close()