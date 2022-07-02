import time
import rpyc

replicas = {
		1: {'SERVER': 'localhost', 'PORT': 6000}, 
		2: {'SERVER': 'localhost', 'PORT': 6001},
		3: {'SERVER': 'localhost', 'PORT': 6002},
		4: {'SERVER': 'localhost', 'PORT': 6003}
		}

def main():
    waiting_neighbors = True
    while waiting_neighbors:
        try:
            conns = []

            # get all nodes
            for replica in replicas:
                conns.append([replica, rpyc.connect(replicas[replica]['SERVER'], replicas[replica]['PORT'])])
            
            waiting_neighbors = False
        except:
            print("Neighbors missing!")
            time.sleep(5)
    
    while(True):
        print("healthCheck")
        time.sleep(60)

if __name__ == "__main__":
	main()