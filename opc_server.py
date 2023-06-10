from opcua import Server
from random import randint
import datetime
import time

url = "opc.tcp://192.168.0.8:4840"
server = Server()
server.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

Temp = Param.add_variable(addspace, "Temperature", 0)
Press = Param.add_variable(addspace, "Pressure", 0)
Time = Param.add_variable(addspace, "Time", 0)

Temp.set_writable()
Press.set_writable()
Time.set_writable()

server.start()
print("Server started ad {}".format(url))

while True:

    Temperature = randint(10, 50)
    Pressure = randint(200,999)
    Chrono = datetime.datetime.now()

    print(Temperature, Pressure, Chrono)

    Temp.set_value(Temperature)
    Press.set_value(Pressure)
    Time.set_value(Chrono)

    time.sleep(.5)
