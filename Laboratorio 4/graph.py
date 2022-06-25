import rpyc
from enum import Enum

'''nodes = {
		'a': {'SERVER': 'localhost', 'PORT': 6000, 'NEIGHBORS': ['b', 'j']}, 
		'b': {'SERVER': 'localhost', 'PORT': 6001, 'NEIGHBORS': ['a', 'g', 'c']},
		'c': {'SERVER': 'localhost', 'PORT': 6002, 'NEIGHBORS': ['b', 'e', 'd']},
		'd': {'SERVER': 'localhost', 'PORT': 6003, 'NEIGHBORS': ['c', 'e', 'f']},
		'e': {'SERVER': 'localhost', 'PORT': 6004, 'NEIGHBORS': ['g', 'c', 'd', 'f']},
		'f': {'SERVER': 'localhost', 'PORT': 6005, 'NEIGHBORS': ['e', 'd', 'i']},
		'g': {'SERVER': 'localhost', 'PORT': 6006, 'NEIGHBORS': ['b', 'j', 'e', 'h']},
		'h': {'SERVER': 'localhost', 'PORT': 6007, 'NEIGHBORS': ['g', 'i']},
		'i': {'SERVER': 'localhost', 'PORT': 6008, 'NEIGHBORS': ['h', 'f']},
		'j': {'SERVER': 'localhost', 'PORT': 6009, 'NEIGHBORS': ['a', 'g']}
		}'''

nodes = {
		'a': {'SERVER': 'localhost', 'PORT': 6000, 'NEIGHBORS': ['b', 'c']}, 
		'b': {'SERVER': 'localhost', 'PORT': 6001, 'NEIGHBORS': ['a', 'd']},
		'c': {'SERVER': 'localhost', 'PORT': 6002, 'NEIGHBORS': ['a', 'd']},
		'd': {'SERVER': 'localhost', 'PORT': 6003, 'NEIGHBORS': ['b', 'c']}
		}

class Status(Enum):
    FREE = 0
    ELECTION = 1

def getNumberOfNeighbors(node):
    return len(nodes[node]['NEIGHBORS'])

def getPort(node):
    return nodes[node]['PORT']

def getServer(node):
    return nodes[node]['SERVER']    

def startClientConnections(node):
	conns = []

	# get neighbors
	neighbors = nodes[node]['NEIGHBORS']
	for ngh in neighbors:
		conn = [ngh, rpyc.connect(nodes[ngh]['SERVER'], nodes[ngh]['PORT'])]
		conns.append(conn)
	return conns

def startAllServerNodesConnections():
    conns = []

	# get all nodes
    for node in nodes:
        conns.append([node, rpyc.connect(nodes[node]['SERVER'], nodes[node]['PORT'])])
	
    return conns

def startAllServerOtherNodesConnections(node):
    conns = []

	# get all nodes
    for nd in nodes:
        if (nd != node):
            conns.append([nd, rpyc.connect(nodes[nd]['SERVER'], nodes[nd]['PORT'])])
	
    return conns    

def getNodeInput():
	invalid_input = True
	node = ''

	while (invalid_input):
		invalid_input = False
		msg = input("Type wich node you want (a to j): ")

		if (len(msg) == 0 or len(msg) > 1):
			print("Invalid input. Try again!")
			invalid_input = True
			continue

		ascii_value = ord(msg)
		if ((ascii_value >= 97 and ascii_value <= 106) or (ascii_value >= 65 and ascii_value <= 74)):
			node = ascii_value
		else:
			print("Invalid input. Try again!")
			invalid_input = True

	return chr(node)
