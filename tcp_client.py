import socket
import threading
import csv

# Define the server host and port
HOST = 'localhost'
PORT = 12345
terminate = False
mutex = threading.Lock()

def SenderClient():

    global terminate

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    while not terminate:
        # Get user input
        level_input = float(input("Enter the tank level: "))

        # Send data to the server
        client_socket.send(str(level_input).encode('utf-8'))

        # Check if termination code sent
        if level_input == 0.0:
            print("Termination code sent. Closing the connection.")
            mutex.acquire()
            terminate = True
            mutex.release()

    # Close the connection
    client_socket.close()

def ReceiverClient():

    global terminate

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT+1))
    print(f"Connected to {HOST}:{PORT+1}")

    csv_file = 'data.csv'
    field_names = ['Ciclo',u'Saída']

    with open(csv_file, mode='w', newline='') as file:
        
        # Create a CSV writer object
        writer = csv.writer(file)
        
        writer.writerow(field_names)
        
        while not terminate:

            response = client_socket.recv(1024).decode('utf-8')
            if response == '':
                response = "0,.0"
            my_array = response.split(',')
            arr = []
            arr.append(int(my_array[0]))
            arr.append(float(my_array[1]))
            writer.writerow(arr)
            arr.clear()

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