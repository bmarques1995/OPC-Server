import socket

# Define the server host and port
HOST = 'localhost'
PORT = 12345

# Define the termination code
TERMINATION_CODE = 'exit'

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
    print(f"Received data: {data}")

    # Check if termination code received
    if data.strip().lower() == TERMINATION_CODE:
        print("Termination code received. Closing the connection.")
        break

    # Send a response to the client
    response = "Server received: " + data
    client_socket.send(response.encode('utf-8'))

# Close the connection
client_socket.close()
server_socket.close()