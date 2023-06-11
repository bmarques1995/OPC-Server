import datetime
import socket
import threading
from time import sleep
from opcua import Client

# Define the server host and port
HOST = '127.0.0.1'
PORT = 12345

level_input = 0.5
mutex = threading.Lock()

def ReceiverServer():

    field_names = ['Saída']

    global level_input

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        if data == '':
            data = ".0"
        data = float(data)
        mutex.acquire()
        level_input = float(data)
        mutex.release()
        print(f"Received data: {data}")

        # Check if termination code received
        if data == 0.0:
            print("Termination code received. Closing the connection.")
            break

    # Close the connection
    client_socket.close()
    server_socket.close()
    

def SenderServer():
    global level_input

    counter = 1

    opc_url = "opc.tcp://127.0.0.1:4850"
    opc_client = Client(opc_url)
    opc_client.connect()
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT+1))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT+1}")

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:

        start_time = datetime.datetime.now()
        # Check if termination code received
        mutex.acquire()
        data = level_input
        mutex.release()

        if data == 0.0:
            print("Termination code received. Closing the connection.")
            break

        Lev = opc_client.get_node("ns=2;i=3")
        Level = Lev.get_value()
        Ref = opc_client.get_node("ns=2;i=2")
        Ref.set_value(1)
        response = str(counter) + ',' + str(Level)
        client_socket.send(response.encode('utf-8'))
        sleep(.01 - (datetime.datetime.now()-start_time).total_seconds())
        counter = counter+1

    # Close the connection
    client_socket.close()
    server_socket.close()
    opc_client.disconnect()

# Create and start the threads
thread1 = threading.Thread(target=ReceiverServer)
thread2 = threading.Thread(target=SenderServer)

thread1.start()
thread2.start()

# Wait for the threads to finish
thread1.join()
thread2.join()