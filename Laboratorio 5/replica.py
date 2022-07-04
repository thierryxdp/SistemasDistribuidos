''' 
	THIERRY PIERRE DUTOIT
    07-01-2022
    LAB 5 - CONSISTENCY AND REPLICATION
'''

replicas = {
		1: {'SERVER': 'localhost', 'PORT': 6000}, 
		2: {'SERVER': 'localhost', 'PORT': 6001},
		3: {'SERVER': 'localhost', 'PORT': 6002},
		4: {'SERVER': 'localhost', 'PORT': 6003}
		}

import socket, threading, select, sys

MAX_CONNECTIONS = 3
MESSAGE_SIZE = 2048

inputs = [sys.stdin]
local_history = []
global_history = []

X = 0
ID = 0
isPrimaryCopy = False

def send_msg(replicaID, message):
    sock = socket.socket()
    sock.connect((getServer(replicaID), getPort(replicaID)))
    msg = message.encode("utf-8")
    sock.sendall(msg)
    sock.close()

def send_recv_msg(replicaID, message):
    sock = socket.socket()
    sock.connect((getServer(replicaID), getPort(replicaID)))
    msg = message.encode("utf-8")
    sock.sendall(msg)
    full_msg = sock.recv(MESSAGE_SIZE)
    message =  full_msg.decode("utf-8")
    sock.close()
    return message

def has_primary_copy():
    global isPrimaryCopy
    string_msg = ""
    if isPrimaryCopy:
        string_msg = "True"
    else:
        string_msg = "False"
    return string_msg

def get_primary_copy():
        global isPrimaryCopy
        global global_history
        global local_history
        
        isPrimaryCopy = False

        # att global_history
        if len(local_history) > 0:
            global_history.append(local_history[-1])

        # send global_history to all replicas
        for replica in replicas:
            if replica != ID:
                try:
                    if len(global_history) > 0:
                        send_msg(replica, str(global_history))
                except:
                    pass
        
def att_global_history(pc_global_history):
    global global_history
    global X
    global_history = []
    for update in pc_global_history.strip("][").split(", "):
        update = update.strip("\'")
        global_history.append(update)
    last_update = global_history[-1].split(" ")
    X = int(last_update[5])
    
def requisition(newSock, address):

    while True:
        full_msg = newSock.recv(MESSAGE_SIZE)
        message =  full_msg.decode("utf-8")

        if not message:
            newSock.close()
            return
        else:
            if message == "has_primary_copy":
                string_msg = has_primary_copy()
                byte_msg = string_msg.encode("utf-8")
                newSock.sendall(byte_msg)                    
            elif message == "get_primary_copy":
                get_primary_copy()
            else:
                att_global_history(message)
            

def getReplicaID():
    invalid_input = True
    
    while (invalid_input):
        invalid_input = False
        id = int(input("Type which replica you want to be (from 1 to 4): "))

        if (id < 1 or id > 4):
            print("Invalid input. Try again!")
            invalid_input = True
            continue
    
    global ID
    ID = id

    if (id == 1):
        global isPrimaryCopy
        isPrimaryCopy = True

def getPort(replicaID):
    return replicas[replicaID]['PORT']

def getServer(replicaID):
    return replicas[replicaID]['SERVER']

def optionOne():
    print("Current value of X: " + str(X) + "\n")

def optionTwo():

    print("History of Global changes of X: \n")
    holder = global_history
    for update in holder:
        print(update)

    print("\nHistory of Local changes of X: \n")
    for update in local_history:
        print(update)
    print("")

def getPrimaryCopy():
    global isPrimaryCopy
    isPrimaryCopy = True
    
    for replica in replicas:
        if (replica != ID):
            try:
                if send_recv_msg(replica, "has_primary_copy") == "True":
                    send_msg(replica, "get_primary_copy")
            except:
                pass

def optionThree():
    global X
    global local_history

    X = int(input(("Type the value of X to be overwritten: ")))

    update = "Value of X updated to " + str(X) + " by replica [" + str(ID) + "]"
    local_history.append(update)

    getPrimaryCopy()
    
    print("Value successfuly overwritten! Now X has value of: " + str(X) + "\n")

def optionFour():
    print("ended!")

def interface(option):
    while True:
        if option == 1:
            optionOne()
            return 1
        elif option == 2:
            optionTwo()
            return 2   
        elif option == 3:
            optionThree()
            return 3
        elif option == 4:
            optionFour()
            return 4
        else:
            print("\nInvalid option. Try again!")
            print("input option: ")
            option = int(input())
            print("")

def createServerConnection():
    # create socket (instantiation)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind port and interface to communicate with clients
    sock.bind((getServer(ID), getPort(ID)))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set max number of connections and wait for at least one connection
    sock.listen(MAX_CONNECTIONS)

    sock.setblocking(False)

    inputs.append(sock)

    return sock

def printOptions():
    print("Choose an option with the buttons below:")
    print("Option (1): Get current value of X")
    print("Option (2): Get History of changes of X")
    print("Option (3): Overwrite value of X")
    print("Option (4): End Program")
    print("input option: ")    

def main():
    
    threads = []
    
    getReplicaID()
    
    print("id: " + str(ID))

    passiveSock = createServerConnection()
    
    printOptions()
    
    while True:
        r, escrita, excecao = select.select(inputs, [], [])
        
        for ready in r: 
            if ready == passiveSock:
                newSock, address = passiveSock.accept()
                
                newThread = threading.Thread(
                    target=requisition, args=(newSock, address))
                newThread.start()
                threads.append(newThread)
            elif ready == sys.stdin:
                option = int(input())
                print("")
                option = interface(option)
                if (option == 4):
                    for t in threads:
                        t.join()
                    passiveSock.close()
                    sys.exit()
                else:
                    print("input option: ")

if __name__ == "__main__":
	main()