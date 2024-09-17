import sys
import socket 

# From command argument
CLIENT = sys.argv[1] # specified client
HOST = sys.argv[2] # specified host
PORT = int(sys.argv[3]) # specified port
NUM_MSG = sys.argv[4] # num msg to show

# Create socket 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

message = input("Enter your message: ")
