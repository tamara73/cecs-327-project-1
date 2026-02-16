import socket

# this will connect it to own computers ip address
HOST = "127.0.0.1"
PORT = 8080

#create socket and connects to app server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    #convert raw socket bytes into readable / writable text
    rfile = s.makefile("r", encoding="utf-8", newline="\n")
    wfile = s.makefile("w", encoding="utf-8", newline="\n")

    print("Connected! Type LIST or SEARCH city=... and max_price=...")
    print("Type 'quit' to exit...")

    while True:
        #ask user for input
        message = input("Client: ")

        #if user wnats to quit it will noify server and stop client
        if message.strip().lower() == "quit":
            wfile.write("quit\n")
            wfile.flush()
            print("Disconnecting... bye bye!")
            break

        #sends command to app server
        wfile.write(message + "\n")
        wfile.flush()
        #stops untill end or error
        lines = []
        while True:
            line = rfile.readline()
            if not line:
                break
            lines.append(line.strip())
            #stop read when result block finishes
            if line.startswith("ERROR") or line.strip() == "END":
                break

        print("Server:")
        for i in lines:
            print(i)