from opcua import Server
from random import random
import datetime
import time

class OpenBlock:
    def __init__(self):
        self.LastInput = .0
        self.LastOutput = .0

    def GetOutput(self, arg_input):
        output = .0306*self.LastInput + .9235*self.LastOutput

        self.LastInput = (arg_input)
        self.LastOutput = output
        return output

sys = OpenBlock()

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

Free = Param.add_variable(addspace, "CanWrite", False)
Free.set_writable()

Fin = Param.add_variable(addspace, "Finish", False)
Fin.set_writable()
Finish = Fin.get_value()

server.start()
print("Server started ad {}".format(url))

while not Finish:
    start_time = datetime.datetime.now()

    if(Free.get_value()):
        Level = sys.GetOutput(Ref.get_value())
        Lev.set_value(Level)
        Free.set_value(False)

    Finish = Fin.get_value()

server.stop()
