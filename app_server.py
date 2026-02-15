import socket

APP_HOST = "0.0.0.0"
APP_PORT = 8080

DATA_HOST = "127.0.0.1"
DATA_PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((APP_HOST, APP_PORT))
server.listen(1)

print(f"[app_server] Listening on {APP_HOST}:{APP_PORT}")
print(f"[app_server] Will forward to data_server at {DATA_HOST}:{DATA_PORT}")

while True:
    client_conn, client_addr = server.accept()
    print(f"[app_server] Client is connected: {client_addr}")

    cr = client_conn.makefile("r", encoding="utf-8", newline="\n")
    cw = client_conn.makefile("w", encoding="utf-8", newline="\n")

    try:
        while True:
            line = cr.readline()
            if not line or line.strip() == "quit":
                break
            
            # ensures that we actually check for a query being sent and also strips query request
            query = line.strip()
            if not query:
                continue

            query = line.strip()
            print(f"[app_server] Received from client: {query}")

            # Connect to data_server for this request ds = data_server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ds:
                ds.connect((DATA_HOST, DATA_PORT))
                ds_r = ds.makefile("r", encoding="utf-8", newline="\n")
                ds_w = ds.makefile("w", encoding="utf-8", newline="\n")

                ds_w.write(query + "\n")
                ds_w.flush()

                ds_response = ds_r.readline().strip()
                print(f"[app_server] Got from data_server: {ds_response}")

            # Send back to client
            cw.write(ds_response + "\n")
            cw.flush()

    finally:
        client_conn.close()
        print("[app_server] Client connection is closed, bye bye!")
