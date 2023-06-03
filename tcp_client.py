import socket

# Define the server host and port
HOST = 'localhost'
PORT = 12345

# Define the termination code
TERMINATION_CODE = 'exit'

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

while True:
    # Get user input
    message = input("Enter a message ('exit' to terminate): ")

    # Send data to the server
    client_socket.send(message.encode('utf-8'))

    # Check if termination code sent
    if message.strip().lower() == TERMINATION_CODE:
        print("Termination code sent. Closing the connection.")
        break

    # Receive and print the server's response
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {response}")

# Close the connection
client_socket.close()