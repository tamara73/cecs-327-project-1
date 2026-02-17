import socket
import time

# this will connect it to own computers ip address
HOST = "127.0.0.1"
PORT = 8080

# Simple Performance Experiment (Real-Life Angle) - this will run the command 50 times
def performace_test(wfile, rfile):
    command = "SEARCH city=LA max_price=5000"
    repeats = 50

    print("\nRunning performance test...")
    print(f"Sending '{command}' {repeats} times...\n")
    start = time.time()

    for i in range(repeats):
        #send request
        wfile.write(command + "\n")
        wfile.flush()
        #reads until END
        while True:
            line = rfile.readline()
            if not line:
                break
            if line.startswith("ERROR") or line.strip() == "END":
                break
    end = time.time()
    total = end - start
    avg = total / repeats

    print(f"Total time: {total:.6f} seconds")
    print(f"Average per request: {avg:.6f} seconds\n")

#create socket and connects to app server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    #convert raw socket bytes into readable / writable text
    rfile = s.makefile("r", encoding="utf-8", newline="\n")
    wfile = s.makefile("w", encoding="utf-8", newline="\n")

    print("Connected! \nType 'LIST' to see all listings\nType SEARCH city=... max_price=...")
    print("Type 'QUIT' to exit")

    while True:
        #ask user for input
        message = input("Client: ").strip()

        if not message:
            continue

        if message.upper() == "PERF":
            performace_test(wfile, rfile)
            continue

        #if user wants to quit it will noify server and stop client
        if message.upper() == "QUIT":
            wfile.write("QUIT\n")
            wfile.flush()
            print("Disconnecting... bye bye!")
            break

        #sends command to app server
        wfile.write(message + "\n")
        wfile.flush()
        #stops until end or error
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
