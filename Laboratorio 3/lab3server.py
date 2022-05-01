import socket
import operator
import json

# multiprocessing
import select
import threading
import sys

HOST = ''          # Any address will be able to reach server side
DOOR = 5000        # Door used by both client/server

MESSAGE_SIZE = 1024
MAX_CONNECTIONS = 5
DICT_RETURN_SIZE = 5

inputs = [sys.stdin]


def createServerConnection():
    # create socket (instantiation)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind door and interface to communicate with clients
    sock.bind((HOST, DOOR))

    # Set max number of connections and wait for at least one connection
    sock.listen(MAX_CONNECTIONS)

    sock.setblocking(False)

    inputs.append(sock)

    return sock


def requisition(newSock, address):
    while True:
        # Keep blocked until receives message from client side
        message = newSock.recv(MESSAGE_SIZE)
        # If client side doesn't send a message end communication
        if not message:
            print(str(address) + '-> ended')
            newSock.close()  # encerra a conexao com o cliente
            return
        else:
            print("Message received from (" + str(address[1]) + "): " +
                  str(message, encoding='utf-8'))

            file_name = str(message, encoding='utf-8')

            try:
                file = data_acess(file_name)

                if (file):
                    ans = data_process(file)

                    # Send the same message received to client side
                    newSock.send(
                        bytes("Most common words from file: " + str(ans), encoding='utf-8'))
            except Exception as error:
                newSock.send(bytes(str(error), encoding='utf-8'))


def interface():

    threads = []
    passiveSock = createServerConnection()

    print("Accepting Connections...")

    while True:
        r, escrita, excecao = select.select(inputs, [], [])

        for ready in r:
            if ready == passiveSock:
                newSock, address = passiveSock.accept()
                print("On " + str(address[0]) +
                      " connecting with " + str(address[1]))

                newThread = threading.Thread(
                    target=requisition, args=(newSock, address))
                newThread.start()
                threads.append(newThread)
            elif ready == sys.stdin:
                command = input()
                if (command == 'exit'):
                    for t in threads:
                        t.join()
                    passiveSock.close()
                    sys.exit()


def data_acess(file_name):
    try:
        file = open(file_name, "r", encoding='utf-8')
        return file
    except FileNotFoundError as ferror:
        raise FileNotFoundError(ferror)


def data_process(file):
    text = file.read()

    # process text
    text = text.lower()

    word_dict = {}
    for word in text.split():
        if not (word_dict.get(word)):
            word_dict[word] = 0
        word_dict[word] += 1

    sorted_dict = dict(
        sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True))

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
