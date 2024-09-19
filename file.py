import os

file_path = 'database.txt'

if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        # Create a new file and write something to it (optional)
        f.write('Welcome to Discordn\'t. Start chatting here')
    print(f'File {file_path} created.')

else:
    with open(file_path,'r') as f:
        chat = f.read()
        print(chat)