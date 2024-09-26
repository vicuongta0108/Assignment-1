import socket
import sys
import select
import os
import termios

USERNAME = 'tavc' # sys.argv[1]
HOST = 'localhost'# sys.argv[2]
PORT = 3001 # int(sys.argv[3])
NUM_MSG = int(sys.argv[4]) if len(sys.argv) > 4 else 50 # number of latest messages, retrieve 50 newest messages if not passed in

# create an INET, STREAMing socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

user_input = ''
chat_history = []

def handleChatHistory(data):
    lines = data.strip().split('\n')
    for line in lines:
        if ': ' in line:
            username, message = line.split(': ', 1)
            chat_history.append({"username": username, "message": message.strip()})

def loadChat(chat, num):
    newest_message = chat[-num:] if num else chat
    for message in newest_message:
        print(f"{message['username']}: {message['message']}")
        
def setNonCanonicalMode():
    fd = sys.stdin.fileno()
    oldattr = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON
    newattr[3] = newattr[3] & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    return oldattr

def restoreCanonicalMode(oldattr):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSANOW, oldattr)

try:
    oldattr = setNonCanonicalMode()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        loadChat(chat_history, NUM_MSG)
        print('>>', user_input, end='', flush = True)
        
        readable, writable, exceptional = select.select([sys.stdin, client_socket], [], [sys.stdin, client_socket])
        for source in readable:
            # print existing messages received from server
            if source is client_socket:
                data = client_socket.recv(1024).decode()
                if data:
                    handleChatHistory(data)
                else:
                    print('Server disconnected')
                    client_socket.close()
                    sys.exit(0)
            elif source is sys.stdin:
                # Handle user input from stdin
                char = sys.stdin.read(1)
                if char.lower() == 'q':  # Allow user to exit by typing 'q'
                    print('\nQuitting!')
                    client_socket.close()
                    sys.exit(0)
                elif char == '\n': # User pressed enter (send message)
                    message = f'{USERNAME}: {user_input}'
                    client_socket.send(message.encode())  # Send message to the server
                    user_input = '' # reset for next input
                elif char == '\b': # User pressed backspace (delete char)
                    user_input = user_input[:-1]
                else: # store char to current input
                    user_input += char

except KeyboardInterrupt:
    print("\nReceived KeyboardInterrupt, exiting...")
except Exception as e:
    print('Error:', e)
finally:
    client_socket.close()
    sys.exit(0) # successful termination