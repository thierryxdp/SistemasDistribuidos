#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Cliente de echo usando RPC
import rpyc #modulo que oferece suporte a abstracao de RPC

# endereco do servidor de echo
SERVIDOR = 'localhost'
PORTA = 10001

def iniciaConexao():
	'''Conecta-se ao servidor.
	Saida: retorna a conexao criada.'''
	conn = rpyc.connect(SERVIDOR, PORTA) 
	
	print(type(conn.root)) # mostra que conn.root eh um stub de cliente
	print(conn.root.get_service_name()) # exibe o nome da classe (servico) oferecido

	return conn

def fazRequisicoes(conn):
	'''Faz requisicoes ao servidor e exibe o resultado.
	Entrada: conexao estabelecida com o servidor'''
	# le as mensagens do usuario ate ele digitar 'fim'
	while True: 
		msg = input("Digite uma mensagem ('fim' para terminar):")
		if msg == 'fim': break 

		# envia a mensagem do usuario para o servidor
		ret = conn.root.exposed_echo(msg)

		# imprime a mensagem recebida
		print(ret)

	# encerra a conexao
	conn.close()

def main():
	'''Funcao principal do cliente'''
	#inicia o cliente
	conn = iniciaConexao()
	#interage com o servidor ate encerrar
	fazRequisicoes(conn)

# executa o cliente
if __name__ == "__main__":
	main()