import sys
import socket
import select
import os

PORT = 3000

# Create a server socket to listen to incoming messages
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Non-blocking, so that select can deal with the multiplexing
server_socket.setblocking(False)

# Bind the socket to a public host, and a well-known port
hostname = socket.gethostname()
server_socket.bind((hostname, PORT)) # connect 
server_socket.listen(5)

inputs = [server_socket] # store all logged in clients here 
outputs = [] # send to (other) clients 

def handleChat(message):
    # Check file existence
    file_path = 'database.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('Welcome to Discordn\'t. Start chatting here\n') 
    else:
        # Append new message to the file
        with open(file_path, 'a') as f:
            f.write(message + '\n')
        # Send updated chat to all connected clients
        with open(file_path, 'r') as f:
            chat = f.read()
            for client in inputs[1:]: # skip the server socket
                client.sendall(chat.encode())

print('Starting Discordn\'t...')
while True:
    try:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for source in readable:
            if source is server_socket:
                client_socket, client_addr = server_socket.accept()
                inputs.append(client_socket)
                with client_socket:
                    data = client_socket.recv(1024)
                    handleChat(data.encode())
            else:
                print('Heard sth else')
                        
    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt, exiting...")
    except Exception as e:
        print('Error:', e)
    finally:
        server_socket.close()
        sys.exit(0) # successful termination
        print('Closing socket! Exiting!')