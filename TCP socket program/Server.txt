# Import the socket module
import socket

# Function to reverse a string
def reverse_message(msg):
    return msg[::-1]

# Server IP address and port number
srv_ip = ''
srv_port = 5002 

# Use try block to catch exception
try:
    # Create a socket object for the server
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the IP address and port
    srv_socket.bind((srv_ip, srv_port))
    # Listen for incoming connections
    srv_socket.listen(1)

    # Use while loop to handle multiple client connections
    while True:
        # Accept a connection from the client
        cli_socket, cli_address = srv_socket.accept()
        print(f"Connected to {cli_address}")

        # Use while loop to receive and process messages from the client
        while True:
            # Read data from client and store it in variable msg
            msg = cli_socket.recv(1024).decode()

            # Use if statement to check if the received message is "end"
            if msg == "end":
                # If yes, send "dne" to the client
                cli_socket.send("dne".encode())
                # Read response from the client and store it in variable resp
                resp = cli_socket.recv(1024).decode()
                # Use if statement to check if the response message is "end"
                if resp == "dne":
                    # If yes, close the client socket
                    cli_socket.close()
                    print(f"Connection to {cli_address} closed.")
                    break
            else:
                # Reverse the received message
                reversed_msg = reverse_message(msg)
                # Send the reversed message to the client
                cli_socket.send(reversed_msg.encode())

except Exception as e:
    # Display a message to handle any exceptions occur within the try block
    print("An error occurred:", e)

finally:
    # Close the server socket
    srv_socket.close()