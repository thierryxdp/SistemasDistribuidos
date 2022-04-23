import socket
import operator
import json

HOST = ''          # Any address will be able to reach server side
DOOR = 5000        # Door used by both client/server

MESSAGE_SIZE = 1024
MAX_CONNECTIONS = 1
DICT_RETURN_SIZE = 5

def interface():
    # create socket (instantiation)
    passiveSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind door and interface to communicate with clients
    passiveSock.bind((HOST, DOOR))

    # Set max number of connections and wait for at least one connection
    passiveSock.listen(MAX_CONNECTIONS)

    # Stay blocked until the first connection is made
    newSock, address = passiveSock.accept()

    print("On " + str(address[0]) + " connecting with " + str(address[1]))

    while True:
        while True:
            # Keep blocked until receives message from client side
            message = newSock.recv(MESSAGE_SIZE)
            # If client side doesn't send a message end communication
            if not message:
                break
            else:
                print("Message received from (" + str(address[1]) + "): " + 
                    str(message, encoding='utf-8'))
                
                file_name = str(message, encoding='utf-8')

                try:
                    file = data_acess(file_name)

                    if (file):
                        ans = data_process(file)
                        # Send the same message received to client side
                        newSock.send(bytes("Most common words from file: " + json.dumps(dict(ans)), encoding='utf-8'))
                except Exception as error:
                    newSock.send(bytes(str(error), encoding='utf-8'))

        newSock.close()

        print("On " + str(address[0]) + " closing connection with " + str(address[1]))

        newSock, address = passiveSock.accept()

        print("On " + str(address[0]) + " connecting with " + str(address[1]))

    # Keep Running and Never Closes Connection
    passiveSock.close()

def data_acess(file_name):
    try:
        file = open(file_name, "r")
        return file
    except FileNotFoundError as ferror:
        raise FileNotFoundError(ferror)

def data_process(file):
    text = file.read()
    
    word_dict = {}
    for word in text.split():
        if not (word_dict.get(word)):
            word_dict[word] = 0
        word_dict[word] += 1
    
    sorted_dict = dict( sorted(word_dict.items(), key=operator.itemgetter(1),reverse=True))
    
    ans = []
    counter = 0
    for pair in sorted_dict.items():
        ans.append(pair)
        counter += 1
        if (counter == DICT_RETURN_SIZE):
            break
    return ans

def main():
    interface()

if __name__ == "__main__":
    main()
        
