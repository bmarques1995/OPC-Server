from opcua import Server
from random import random
import datetime
import time

url = "opc.tcp://127.0.0.1:4850"
server = Server()
server.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

Ref = Param.add_variable(addspace, "Reference", 0)
Ref.set_writable()

Lev = Param.add_variable(addspace, "Level", 1)
Lev.set_writable()

server.start()
print("Server started ad {}".format(url))

while True:

    Level = random()
    Lev.set_value(Level)

    print(Lev.get_value(), Ref.get_value())

    time.sleep(.1)
