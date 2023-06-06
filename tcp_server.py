import socket
import threading

# Define the server host and port
HOST = 'localhost'
PORT = 12345

level_input = 0.0
mutex = threading.Lock()

def ReceiverServer():

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

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT+1))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:

        # Check if termination code received
        mutex.acquire()
        data = level_input
        mutex.release()

        if data == 0.0:
            print("Termination code received. Closing the connection.")
            break

        response = "Server received: "
        mutex.acquire()
        response = "Server received: " + str(level_input)
        mutex.release()
        client_socket.send(response.encode('utf-8'))

    # Close the connection
    client_socket.close()
    server_socket.close()

# Create and start the threads
thread1 = threading.Thread(target=ReceiverServer)
thread2 = threading.Thread(target=SenderServer)

thread1.start()
thread2.start()

# Wait for the threads to finish
thread1.join()
thread2.join()