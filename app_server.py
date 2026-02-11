import socket


def handle_request(request):
    # we need to process request and return a response here
    return

# Gets ip address from local computer (might need to replace later)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

# Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

while True:
    # Allows us to accept one client at a time
    client, address = server.accept()
    print(f"Connection from: {address}")    
    # Handle request
    data = client.recv(1024).decode('utf-8')
    response = handle_request(data)
    client.send(response.encode('utf-8'))

    # Close and move to next client
    client.close()