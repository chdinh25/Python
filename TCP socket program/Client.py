# Import the socket module
import socket

# Server IP address and port number
srv_ip = ''
srv_port = 5002

# Use try block to catch exception
try:
    # Create a socket object for the client
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     # Connect to the server
    cli_socket.connect((srv_ip, srv_port))

    # Use while loop to interact with the server
    while True:
        # Prompt client to input and store it in variable msg
        msg = input("Enter a message or type 'end' to stop: ")
        # Send the message to the server
        cli_socket.send(msg.encode())
        # Use if statement to check if the received message is "end"
        if msg == "end":
            # Read response from the client and store it in variable resp
            resp = cli_socket.recv(1024).decode()
            # Use if statement to check if the response message is "end"
            if resp == "dne":
                # If yes, display end statement
                print("Client terminated.")
                # Close the client socket
                cli_socket.close()
                break
        else:
            # Receive reversed message from the server
            reversed_resp = cli_socket.recv(1024).decode()
            # Display reversed message received from the server
            print("Reversed message:", reversed_resp)

except Exception as e:
    # Display a message to handle any exceptions occur within the try block
    print("An error occurred:", e)

finally:
    # Close the client socket
    cli_socket.close()