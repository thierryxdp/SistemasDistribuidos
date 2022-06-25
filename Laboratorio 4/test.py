from graph import startAllServerNodesConnections, getNodeInput

import time

def interface(conns):

	# le as mensagens do usuario ate ele digitar 'fim'
    print("All neighbors connected!")
    while True: 
        msg = input("Type a message ('end' to terminate program): ")
        if msg == 'end': 
            break
        if msg == 'election':
            node = getNodeInput()

            for conn in conns:
                if (conn[0] == node):
                    conn[1].root.exposed_start_election(conn[0])			

    for conn in conns:
        conn[1].close()

if __name__ == "__main__":

    waiting_neighbors = True
    while waiting_neighbors:
        try:
            conns = startAllServerNodesConnections()
            waiting_neighbors = False
        except:
            print("Neighbors missing!")
            time.sleep(5)

    interface(conns)