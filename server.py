import sys
import socket
import select

# Create a server socket to listen to incoming messages
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Non-blocking, so that select can deal with the multiplexing
server_socket.setblocking(False)
# Bind the socket to a public host, and a well-known port
hostname = server_socket.getsockname()
server_socket.bind(hostname, 80) # connect 

inputs = [server_socket] # store all logged in clients here 
outputs = [] # send to (other) clients 

while True:
    try:
        print('Working on a startup...')
        readable, writeable, exception = select.select(inputs, outputs, inputs)
        for source in readable:
            data, addr = source.recvfrom(1024)
            print(f'Listening to {hostname}:{addr}')

    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt, exiting...")
        server_socket.close()
        sys.exit(0) # successful termination
    except Exception as e:
        print('Error:', e)