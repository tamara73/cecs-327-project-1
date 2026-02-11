import socket

# gets ip address from local computer (might need to replace later)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

while True:
    comm_socket, address = server.accept()
    print(f"Connected to {address}!")
    message = comm_socket.recv(1024).decode('utf-8')
    print(f"Message from client is: {message}")
    comm_socket.send(f"Message received.").encode('utf-8')