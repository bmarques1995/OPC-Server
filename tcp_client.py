import socket
import threading

# Define the server host and port
HOST = 'localhost'
PORT = 12345

def SenderClient():

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    while True:
        # Get user input
        level_input = float(input("Enter the tank level: "))

        # Send data to the server
        client_socket.send(str(level_input).encode('utf-8'))

        # Check if termination code sent
        if level_input == 0.0:
            print("Termination code sent. Closing the connection.")
            break

    # Close the connection
    client_socket.close()

def ReceiverClient():

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT+1))
    print(f"Connected to {HOST}:{PORT}")

    while True:

        # Receive and print the server's response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received response: {response}")

    # Close the connection
    client_socket.close()

# Create and start the threads
thread1 = threading.Thread(target=SenderClient)
thread2 = threading.Thread(target=ReceiverClient)

thread1.start()
thread2.start()

# Wait for the threads to finish
thread1.join()
thread2.join()