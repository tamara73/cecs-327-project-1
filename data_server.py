import socket
import json

# Load data from JSON file
with open('listings.json', 'r') as f:
    listings = json.load(f)

# Gets ip address from local computer (might need to replace later)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

# Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()
print("Data server is running!")

while True:
    client, address = server.accept()

    request = client.recv(1024).decode('utf-8').strip()
    print(f"Request is: {request}")
    
    # Simple response for now (sends all listings)
    if request == "RAW_LIST":
        response = json.dumps(listings)
        client.send(response.encode('utf-8'))

    client.close()