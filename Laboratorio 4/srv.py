#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Servidor de echo usando RPC 
import rpyc #modulo que oferece suporte a abstracao de RPC

#servidor que dispara um processo filho a cada conexao
from rpyc.utils.server import ForkingServer 

# porta de escuta do servidor de echo
PORTA = 10001

# classe que implementa o servico de echo
class Echo(rpyc.Service):
	# executa quando uma conexao eh criada
	def on_connect(self, conn):
		print("Conexao iniciada:")

	# executa quando uma conexao eh fechada
	def on_disconnect(self, conn):
		print("Conexao finalizada:")

	# imprime e ecoa a mensagem recebida
	def exposed_echo(self, msg):
		print(msg)
		return msg

    def exposed_probe(self, msg):
		print(msg)
		return msg    
  
# dispara o servidor
if __name__ == "__main__":
	srv = ForkingServer(Echo, port = PORTA)
	srv.start()


### Tipos de servidores
#https://rpyc.readthedocs.io/en/latest/api/utils_server.html

#servidor que dispara uma nova thread a cada conexao
#from rpyc.utils.server import ThreadedServer

#servidor que atende uma conexao e termina
#from rpyc.utils.server import OneShotServer

### Configuracoes do protocolo RPC
#https://rpyc.readthedocs.io/en/latest/api/core_protocol.html#rpyc.core.protocol.DEFAULT_CONFIG 