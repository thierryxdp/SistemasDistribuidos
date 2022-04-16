import socket

HOST = ''          # Any address will be able to reach server side
DOOR = 5000        # Door used by both client/server

MESSAGE_SIZE = 1024
MAX_CONNECTIONS = 1

# create socket (instantiation)
passiveSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind door and interface to communicate with clients
passiveSock.bind((HOST, DOOR))

# Set max number of connections and wait for at least one connection
passiveSock.listen(MAX_CONNECTIONS)

# Stay blocked until the first connection is made
newSock, address = passiveSock.accept()

while True:
    # Keep blocked until receives message from client side
    message = newSock.recv(MESSAGE_SIZE)
    # If client side doesn't send a message end communication
    if not message:
        newSock.close()
        break
    else:
        print("Messagem Recebida do lado ativo: " +
              str(message, encoding='utf-8'))

    # Send the same message received to client side
    newSock.send(message)

# Close connection
passiveSock.close()
