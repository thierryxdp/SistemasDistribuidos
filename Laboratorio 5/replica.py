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

import rpyc

from rpyc.utils.server import ThreadedServer
import multiprocessing

local_history = []
global_history = []

X = 0
ID = 0
isPrimaryCopy = 0

class Replica(rpyc.Service):

    def exposed_has_primary_copy(self):
        return isPrimaryCopy
    
    def exposed_get_primary_copy(self):
        global isPrimaryCopy
        global global_history
        global local_history
        
        isPrimaryCopy = 0

        # att global_history
        if len(local_history) > 0:
            last_update = local_history[-1]
            global_history.append(last_update)

        # send global_history to all replicas
        for replica in replicas:
            try:
                conn = rpyc.connect(getServer(replica), getPort(replica))
                #print("Achei uma replica: " + str(replica))
                if (replica != ID):
                    #print("atualizando historico global da replica!")
                    #print(global_history)
                    #print(local_history)
                    conn.root.exposed_att_globa_history(global_history)
                conn.close()
            except:
                pass
        
    def exposed_att_globa_history(self, pc_global_history):
        #print("CHEGUEIIIII")
        global global_history
        global_history = pc_global_history

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
        isPrimaryCopy = 1

def getPort(replicaID):
    return replicas[replicaID]['PORT']

def getServer(replicaID):
    return replicas[replicaID]['SERVER']

def createServer(replicaID):
    replicaID = int(replicaID)
    srv = ThreadedServer(Replica, port = getPort(replicaID))
    srv.start()

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

def getPrimaryCopy():
    global isPrimaryCopy
    isPrimaryCopy = 1
    
    for replica in replicas:
        try:
            conn = rpyc.connect(getServer(replica), getPort(replica))
            #print("Achei uma replica: " + str(replica))
            if (replica != ID and conn.root.exposed_has_primary_copy()):
                #print("replica possui copia primaria!")
                conn.root.exposed_get_primary_copy()
            conn.close()
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

def interface():
    print("Choose an option with the buttons below:")
    print("Option (1): Get current value of X")
    print("Option (2): Get History of changes of X")
    print("Option (3): Overwrite value of X")
    print("Option (4): End Program \n")
    while (True):
        option = int(input("input option: "))
        print("\n")
        if option == 1:
            optionOne()
        elif option == 2:
            optionTwo()   
        elif option == 3:
            optionThree()
        elif option == 4:
            optionFour()
            return
        else:
            print("\nInvalid option. Try again!")

def main():
    
    getReplicaID()

    p = multiprocessing.Process(target = createServer,  args=(str(ID)))
    p.start()
    
    interface()

    p.join()

if __name__ == "__main__":
	main()