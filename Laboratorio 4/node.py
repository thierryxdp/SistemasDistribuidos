import rpyc
import sys
import select

from rpyc.utils.server import ForkingServer
import multiprocessing
import time

import os
import sys

from random import seed
from random import randint

nodes = {
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
		}

'''nodes = {
		'a': {'SERVER': 'localhost', 'PORT': 6000, 'NEIGHBORS': ['b', 'c']}, 
		'b': {'SERVER': 'localhost', 'PORT': 6001, 'NEIGHBORS': ['a', 'd']},
		'c': {'SERVER': 'localhost', 'PORT': 6002, 'NEIGHBORS': ['a']},
		'd': {'SERVER': 'localhost', 'PORT': 6003, 'NEIGHBORS': ['b']}
		} '''


MAX_RAND_VALUE = 1000

# classe que implementa o servico de echo
class Node(rpyc.Service):
	ID = randint(0,MAX_RAND_VALUE)
	parent = ''
	
	def exposed_probe(self, parent_node, this_node):

		try:
			f = open("visited.txt", "r+")
			lines = f.read()
			for line in lines:
				if line == this_node:
					f.close()
					return
			
			f.write(this_node)
			f.write('\n')
			f.close()

		except:
			f = open("visited.txt", "w")
			f.write(this_node)
			f.write('\n')
			f.close()

		
		conns = iniciaConexoes(this_node)
		
		visited = []
		
		f = open("visited.txt", "r+")
		lines = f.read()
		for line in lines:
			visited.append(line)

		for conn in conns:
			if (conn[0] not in visited):
				conn[1].root.exposed_probe(this_node, conn[0])
		
		for conn in conns:
			conn[1].close()
		
		conn = rpyc.connect(nodes[parent_node]['SERVER'], nodes[parent_node]['PORT'])

		conn.root.exposed_echo(parent_node, this_node, self.ID)
		
		conn.close()
	
	def exposed_echo(self, this_node, child_node, value):

		max_value = self.ID
		node = this_node
		if value > self.ID:
			max_value = value
			node = child_node

		try:
			f = open("leader.txt", "r")
			line = f.read()
			params = line.split(" ")
			f.close()

			if int(params[1]) < max_value:
				f = open("leader.txt", "w")
				f.write(node + " " + str(max_value))
				f.close()

		except:
			f = open("leader.txt", "w")
			f.write(node + " " + str(max_value))
			f.close()	

def iniciaConexoes(node):
	conns = []

	# pega vizinhos
	neighbors = nodes[node]['NEIGHBORS']
	for ngh in neighbors:
		conn = [ngh, rpyc.connect(nodes[ngh]['SERVER'], nodes[ngh]['PORT'])]
		conns.append(conn)
	return conns

def fazRequisicoes(node, conns):

	# le as mensagens do usuario ate ele digitar 'fim'
	print("All neighbors connected!")
	while True: 
		msg = input("Type a message ('end' to terminate program): ")
		if msg == 'end': break
		if msg == 'election':
			for conn in conns:
				conn[1].root.exposed_probe(conn[0], conn[0])
		if msg == 'remove files':
			removeFiles()				

	# encerra as conexoes
	for conn in conns:
		conn[1].close()

def getNodeInput():
	invalid_input = True
	node = ''

	while (invalid_input):
		invalid_input = False
		msg = input("Type wich node you want to be (a to j): ")
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

def createServer(node):
	#inicia o server para dar apenas uma resposta
	srv = ForkingServer(Node, port = nodes[node]['PORT'])
	srv.start()

def removeFiles():
	os.remove("visited.txt")
	os.remove("leader.txt")

if __name__ == "__main__":

	seed(1)

	node = getNodeInput()

	global this_node
	this_node = node
	
	p = multiprocessing.Process(target = createServer, args=(node))
	p.start()

	conns = []

	waiting_neighbors = True
	while waiting_neighbors:
		try:
			conns = iniciaConexoes(node)
			waiting_neighbors = False
		except:
			print("Neighbors missing!")
			time.sleep(5)
	
	fazRequisicoes(node, conns)

	p.terminate()
	print("End!")