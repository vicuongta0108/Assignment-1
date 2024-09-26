import sys
import socket
import select
import os
import time

PORT = 3001
FILE_PATH = 'chat_history.txt'

# Create a server socket to listen to incoming messages
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Non-blocking, so that select can deal with the multiplexing
server_socket.setblocking(False)

# Bind the socket to a public host, and a well-known port
hostname = '' # socket.gethostname()
server_socket.bind((hostname, PORT)) # connect
server_socket.listen(5)
print(f'Listening on interface {hostname}:{PORT}')

# Statistics
message_recv = 0
message_sent = 0
start_time = time.time()

clients = []
inputs = [server_socket] + clients

def loadChatHistory(path):
    with open(path, 'r') as file:
        chat = file.read()
        return chat

def writeToChat(path, message):
    with open(path, 'a') as file:
        file.write(message + '\n')

def broadcastMessage(message, receiver):
    for r in receiver:
        r.send(message.encode())

def addConnection(source):
    clients.append(source)
    inputs.append(source)

def removeConnection(source):
    clients.remove(source)
    inputs.remove(source)

try:
    # Check file existence and create
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as file:
            pass
        print('Chat History Created!')

    while True:
        print('Waiting for input...')
        readable, writable, exceptional = select.select(inputs, [], inputs)
        for source in readable:
            if source is server_socket: # new client
                client_socket, client_addr = server_socket.accept()
                print(f'New connection at {client_addr}')
                addConnection(client_socket)

                chat_history = loadChatHistory(FILE_PATH)
                if chat_history:
                    client_socket.send(chat_history.encode())
            else:
                print('Heard a client')
                data = source.recv(1024).decode()
                if data:
                    message = data.split(': ', 1)[1].strip()
                    print(f'Message received: {message}')
                    writeToChat(FILE_PATH, data)
                    broadcastMessage(data, clients)
                else:
                    removeConnection(source)

except KeyboardInterrupt:
    print("\nReceived KeyboardInterrupt, exiting...")
except Exception as e:
    print('Error:', e)
finally:
    server_socket.close()
    print('Closing socket! Exiting!')
    sys.exit(0) # successful termination