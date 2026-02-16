import socket

APP_HOST = "0.0.0.0"
APP_PORT = 8080

DATA_HOST = "127.0.0.1"
DATA_PORT = 9090

#cashe will be later

#parase commands from client
def parase_cas_command(line):
    parts = line.split()#spilts the client message into words so we can read the command and its parameters
    if parts[0] == "LIST":#checks if the first word of the command is LIST
        return "LIST", {}
    if parts[0] == "SEARCH":#checks if the first word of the command is SEARCH
        params = {}
        for token in parts[1:]:# loops throught the parameters after SEARCH
            k, v = token.split("=")
            params [k] = v
        return "SEARCH", params
    if parts[0] == "quit":# checks if the client wanst to disconnect/quit
        return "quit", {}
    raise ValueError("unknow command... :(")
    
#translates client command to data server command
def make_ads_command(cmd, params):
    if cmd == "LIST":
        return "RAW_LIST"
    if cmd == "SEARCH":
        return f"RAW_SEARCH city={params['city']} max_price={params['max_price']}"

#reads response untill end or error
def untill_end(rfile):
    lines = []
    while True:#keeps reading line from the data server untill the end of the response
        line = rfile.readline()
        if not line:
            break
        lines.append(line)
        if line.startswith("ERROR") or line.strip() == "END":
            break
    return "".join(lines)

#server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((APP_HOST, APP_PORT))
server.listen(1)

print(f"[app_server] Listening on {APP_HOST}:{APP_PORT}")
print(f"[app_server] Will forward to data_server at {DATA_HOST}:{DATA_PORT}")

while True:
    client_conn, client_addr = server.accept()
    print(f"[app_server] Client is connected: {client_addr}")

    #converts raw socket data into readable text
    cr = client_conn.makefile("r", encoding="utf-8", newline="\n")
    cw = client_conn.makefile("w", encoding="utf-8", newline="\n")

    try:
        while True:
            #reads command from client
            line = cr.readline()
            if not line or line.strip() == "quit":
                break
            
            # ensures that we actually check for a query being sent and also strips query request
            query = line.strip()
            if not query:
                continue

            print(f"[app_server] Received: {query}")

            try:
                cmd, params = parase_cas_command(query)# breaks the clients requst into command tpyes

                if cmd == "quit":
                    break

                #translates client command to data server command
                ads_command = make_ads_command(cmd, params)

                # Connect to data_server for this request ds = data_server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ds:
                    ds.connect((DATA_HOST, DATA_PORT))
                    ds_r = ds.makefile("r", encoding="utf-8", newline="\n")
                    ds_w = ds.makefile("w", encoding="utf-8", newline="\n")

                    #sends translated command
                    ds_w.write(ads_command + "\n")
                    ds_w.flush()

                    #receives multi responses
                    response = untill_end(ds_r)

            except Exception as e: #catches any errors
                cw.write(f"ERROR {e}\n")
                cw.flush()

    finally:
        client_conn.close()
        print("[app_server] Client connection is closed, bye bye!")
