import socket

HOST = 'localhost'  # ip/server to send messages. If it's in another computer, input the ip
DOOR = 5000        # Door used by both client/server

MESSAGE_SIZE = 1024

# create socket (instantiation)
activeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect with client server side
activeSock.connect((HOST, DOOR))

# Keep sending message to server
userInput = input()

while (userInput != "exit"):  # exit will close communication
    encodedMessage = bytes(userInput, encoding='utf-8')
    activeSock.send(encodedMessage)

    # application blocked until receives message
    message = activeSock.recv(MESSAGE_SIZE)

    # Print received message
    print("Messagem Recebida do lado passivo: " +
          str(message, encoding='utf-8'))

    # Keep receiving user input
    userInput = input()


# Close connection
activeSock.close()
