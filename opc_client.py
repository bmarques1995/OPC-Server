from opcua import Client
import time

url = "opc.tcp://127.0.0.1:4850"
client = Client(url)

client.connect()
print("Client Connected")

while True:
    Temp = client.get_node("ns=2;i=2")
    Temperature = Temp.get_value()
    print(Temperature)

    Press = client.get_node("ns=2;i=3")
    Pressure = Press.get_value()
    print(Pressure)

    Chro = client.get_node("ns=2;i=4")
    Chrono = Chro.get_value()
    print(Chrono)

    time.sleep(.25)