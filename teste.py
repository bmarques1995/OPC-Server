from opcua import Client
from opcua.ua import AttributeIds

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (8,4)
import seaborn as sns
sns.set()

##################
# cria o client
client = Client("opc.tcp://localhost:53530/OPCUA/SimulationServer")

client.connect()

# Obtém uma lista de servidores disponíveis na rede
servers = client.find_servers()

##################	
# Imprime a lista de servidores encontrados
for server in servers:
	print("Server URI:", server.ApplicationUri)
	print("Server ProductURI:", server.ProductUri)
	print("Discovery URLs:", server.DiscoveryUrls)
	print("\n")

##################	
node1 = client.get_node("ns=3;i=1008")
node2 = client.get_node("ns=3;i=1003")

plt.ion()
hyst = []

for _ in range(1000):
	
	# le valor
	value = node2.get_value()
	
	# escreve valor
	node1.set_value(value/10.0)

	hyst.append(value)
	
	# Obtenha o nome do nó
	timestamp = node2.get_attribute(AttributeIds.Value)
	print(timestamp)

	##################
	plt.figure(1)
	plt.clf()
	plt.plot(hyst[-50:], 'r*-')
	plt.title('Random:BaseDataVariableType')
	plt.ylim([-2., 2.])
	plt.show()
	plt.pause(1.0)

client.disconnect()
plt.ioff()
