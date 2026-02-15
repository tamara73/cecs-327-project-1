import socket

# this will connect it to own computers ip address
HOST = "127.0.0.1"
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    rfile = s.makefile("r", encoding="utf-8", newline="\n")
    wfile = s.makefile("w", encoding="utf-8", newline="\n")

    print("Connected! Type a city and hit Enter. Type 'quit' to exit.")

    while True:
        message = input("Client: ")

        if message.strip().lower() == "quit":
            wfile.write("quit\n")
            wfile.flush()
            print("Disconnecting... bye bye!")
            break

        wfile.write(message + "\n")
        wfile.flush()

        response = rfile.readline().strip()
        print(f"Server: {response}")