import socket
import sys

USERNAME = sys.argv[2] 
HOST = 'hawk.cs.umanitoba.ca' # localhost if same machine
PORT = 3000 # int(sys.argv[4])

# create an INET, STREAMing socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT)) # hard code server hostname here (might ask for this later)

try: 
    while True:
        text = input()  # prompt user to enter a message
        if text == 'quit':  # allow user to exit by typing 'quit'
            break
        message = f'{USERNAME}: {text}' 
        client_socket.sendall(message.encode())

        # Receive and print chat messages
        data = client_socket.recv(1024) 
        print(data.decode("utf-8") )
except KeyboardInterrupt:
    print("\nReceived KeyboardInterrupt, exiting...")
except Exception as e:
    print('Error:', e)
finally:
    client_socket.close()
    sys.exit(0) # successful termination