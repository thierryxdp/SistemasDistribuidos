''' 
	DONE: Aquivo teste para indicar em qual nó começar a eleição.
	Então, por exemplo, a partir desse arquivo teste, teremos uma conexão
	cliente no Nó indicado a começar a eleição. Esse cliente chamará, por rpc,
	o método do Nó que inicia a eleição.

	Criar uma máquina de estados dentro do No para que saiba se está em processo
	de eleição, se já foi visitado por pobre, se pode mandar o ecko visto que
	todos os filhos já mandaram o echo, etc.

	Colocar as conexões de cada nó dentro da classe Nó, para que ele saiba
	como acessar os vizinhos.

	No arquivo de teste, será possível apenas começar eleição quando todos
	os nós estiverem conectados. Caso contrário, não será  possível começar
	a eleição.

	ir removendo os arquivos em parte. Na real, é melhor criar uma branch
	nova excluindo o uso de arquivos.

	Só responde echo quando todos os vizinhos já tiverem respondido, seja
	por ack ou por echo.

	Os nós vizinhos não terão input. Eles terão apenas o log do que cada um
	está printando. Assim facilita a construção, deixando os inputs apenas
	no arquivo de teste. 
'''

import rpyc

from rpyc.utils.server import ThreadedServer
import multiprocessing

from random import seed
from random import randint

from graph import getNodeInput, getPort, getServer, startClientConnections
from graph import getNumberOfNeighbors, startAllServerOtherNodesConnections, Status

MAX_RAND_VALUE = 100000

id = randint(0,MAX_RAND_VALUE)
parent = ''
status = Status.FREE
returns = 0
max_value = id
leader = ''
	
# classe que implementa o servico de echo
class Node(rpyc.Service):
	
	def exposed_probe(self, calling_node, this_node):

		global parent
		global status
		global returns
		
		if (status == Status.FREE):
			printElectionStarted(id, calling_node, this_node)
			
			status = Status.ELECTION
			parent = calling_node
			returns += 1

			conns = startClientConnections(this_node)

			for conn in conns:
				if (conn[0] != parent):
					conn[1].root.exposed_probe(this_node, conn[0])
			
			for conn in conns:
				conn[1].close()

		elif (status == Status.ELECTION and returns < getNumberOfNeighbors(this_node)):
			printSendingACK(calling_node, this_node)
			conn = rpyc.connect(getServer(calling_node), getPort(calling_node))
			conn.root.exposed_ack(this_node)
			conn.close()
		
		else:
			printSendingEcho(this_node, max_value)
			conn = rpyc.connect(getServer(parent), getPort(parent))
			conn.root.exposed_echo(parent, this_node, max_value)
			conn.close()

			resetValues()

	def exposed_ack(self, node):
		printReceivedACK(node)
		global returns
		returns += 1

	def exposed_echo(self, this_node, child_node, value):
		global returns
		global max_value
		global leader

		printReceivedEcho(this_node, value)

		returns += 1
		if (value > max_value):
			max_value = value
			leader = child_node

		if (returns == getNumberOfNeighbors(this_node)):
			printSendingEcho(this_node, max_value)
			conn = rpyc.connect(getServer(parent), getPort(parent))
			conn.root.exposed_echo(parent, this_node, max_value)
			conn.close()

			resetValues()
	
	def exposed_start_election(self, this_node):
		global status
		global leader
		leader = this_node
		status = Status.ELECTION

		conns = startClientConnections(this_node)
		
		printElectionStarted(id, "raiz", this_node)
		
		for conn in conns:
			conn[1].root.exposed_probe(this_node, conn[0])
		
		for conn in conns:
			conn[1].close()
			
		printElectionResult(leader, max_value)

		conns = startAllServerOtherNodesConnections(this_node)

		for conn in conns:
			conn[1].root.exposed_publish_leader(leader, max_value)
		
		for conn in conns:
			conn[1].close()

		resetValues()

	def exposed_publish_leader(self, node_leader, value_leader):
		printElectionResult(node_leader, value_leader)
		
def printElectionResult(node_leader, value_leader):
	print("Election ended with:")
	print("leader: " + str(node_leader))
	print("max value: " + str(value_leader))
	print("------- Election Ended -------")

def printElectionStarted(node_id, calling_node, this_node):
	print("------ Election Started ------")
	print("ID Node: " + str(node_id))
	print("Node: " + str(this_node) + " received probe from Node: " + str(calling_node))
	print("Parent Node: " + str(calling_node))
	print("")

def printSendingEcho(this_node, max_value):
	print("Node: " + str(this_node) + " sending echo with value: " + str(max_value))
	print("")

def printReceivedEcho(this_node, value):
	print("Node: " + str(this_node))
	print("Received ECHO with value: " + str(value))
	print("")

def printSendingACK(calling_node, this_node):
	print("Node: " + str(this_node) + " sending ack to Node: " + str(calling_node))
	print()

def printReceivedACK(node):
	print("Received ACK from Node: " + str(node))
	print()

def resetValues():
	global id
	global parent
	global status
	global returns
	global max_value
	global leader

	status = Status.FREE
	parent = ''
	returns = 0
	id = randint(0,MAX_RAND_VALUE)
	max_value = id
	leader = ''

def createServer(node):
	#inicia o server para dar apenas uma resposta
	srv = ThreadedServer(Node, port = getPort(node))
	srv.start()

def main():
	seed(1)
	node = getNodeInput()
	p = multiprocessing.Process(target = createServer, args=(node))
	p.start()

	invalid_input = True
	while (invalid_input):
		invalid_input = False
		msg = input("Type 'end' to terminate server: \n")

		if (msg == "end"):
			p.join()
			print("End!")
		else:
			print("Invalid input. Try again!")
			invalid_input = True

if __name__ == "__main__":
	main()