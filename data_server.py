import socket
import json

#loading housing listings from json file
with open("listings.json", "r") as f:
    LISTINGS = json.load(f)


#converts listing dict to format
def listing_to_wire_line(item):
    return (
        f"id={item.get('id')};city={item.get('city')};address={item.get('address')};"
        f"price={item.get('price')};bedrooms={item.get('bedrooms')}"
    )

#parse raw_list / raw_search reqests
def parse_ads_request(line):
    parts = line.strip().split() #removes spaces/newline from the request and splits it into words
    if parts[0] == "RAW_LIST":#will check if the command received is raw_list
        return "RAW_LIST", {}
    
    if parts[0] == "RAW_SEARCH":#ill check if the command received is raw_search
        params = {}
        for token in parts[1:]:#loops through parameters like city=LA and max_price=3000
            k, v = token.split("=")
            params[k] = v
        return "RAW_SEARCH", {
            "city" : params["city"],
            "max_price": int(params["max_price"])
        }
    raise ValueError("unknown command... :(") #raises error

#filters the listings by city and price
def filter_listings(city, max_price):
    return (
        rec for rec in LISTINGS#goes through each listing stored in Listings
        if rec["city"] == city and rec["price"] <= max_price
    )

# okay response 
def ok_response(items):
    lines = [f"OK RESULT {len(items)}\n"]
    for it in items: #loops through each listing result to format and add to response
        lines.append(listing_to_wire_line(it) + "\n")
    lines.append("END\n")
    return "".join(lines)

# error response
def error_response(message):
    return f"ERROR {message}\n"

#handles incoming request
def handle_request(msg):
    try:
        cmd, params = parse_ads_request(msg) #parses incoming request into command and parameters
        if cmd == "RAW_LIST":#if command asks for all listings return everything
            return ok_response(LISTINGS)
        if cmd == "RAW_SEARCH":#if command asks for filtered return filtered
            matches = filter_listings(
                params["city"],
                params["max_price"]
            )
            return ok_response(matches)
    except Exception as e: #this is incase there are any errors
        return error_response(str(e))


#
# This will allow client to search for data in JSON file
# note this implementation is NOT correct rn, it is just filler for testing
#def search(query):
#    return[
#       record for record in LISTINGS
#        if all(str(v).lower() in str(record.get(k, "")).lower() for k, v in query.items())
#   ]

# Setting up host and port
DATA_HOST = "0.0.0.0"
DATA_PORT = 9090

# Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((DATA_HOST, DATA_PORT))
# since we only take one query at a time we only allow
# the server to listen to listen once at a time
server.listen(1) 

# comment to ensure server is connected correctly - can be deleted later
print("Hello, server is ready for your query!")

# This allows for communication between server and client
# Essentially is the mediator, listens to request from client, looks for request, gives client answer, repeats
while True:
    #waits for app server connect
    conn, addr = server.accept()
    print(f"[data_server] Connetion through {addr}")

    # this will turn raw bytes into test that we can read and write to
    rfile = conn.makefile("r", encoding="utf-8", newline="\n")
    wfile = conn.makefile("w", encoding="utf-8", newline="\n")

    try:
        while True:
            line = rfile.readline()
            if not line or line.strip() == "quit":
                break # client wants to disconnect

            msg = line.strip()
            print(f"[data_server] Received: {msg}")

            #made changes here - ashley
            #process request
            response = handle_request(msg)

            #send response back
            wfile.write(response)
            wfile.flush()

    finally:
        conn.close()
        print("[data_server] Connection is closed, bye bye!]")

