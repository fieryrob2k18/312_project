import sys

DEBUG = True

#Read request and send response
def handle_conn(conn):
    parsed_req = read_req(conn)
    #TODO: Hand stuff over to router
    if parsed_req["headers"]["path"] == "/":
        serverfile = open("files/index.html", "rb")
        cnt = serverfile.read()
        cntlen = len(cnt)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: "
        response += str(cntlen) + "\r\n\r\n"
        conn.send(response.encode("utf-8"))
        conn.send(cnt)
    else:
        serverfile = open("files/notfound.html", "rb")
        cnt = serverfile.read()
        cntlen = len(cnt)
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: "
        response += str(cntlen) + "\r\n\r\n"
        conn.send(response.encode("utf-8"))
        conn.send(cnt)
    conn.close()


#Read in header, process then handle body
def read_req(conn):
    stuff = conn.recv(1024)
    while not(bytes("\r\n\r\n", "utf-8") in stuff):
        readin = conn.recv(1024)
        stuff = stuff + readin
    if DEBUG:
        print("Request recieved: ", stuff)
        sys.stdout.flush()
    splitheadbody = stuff.split(bytes("\r\n\r\n", "utf-8"), maxsplit=1)
    headers = parse_headers(splitheadbody[0])
    out = {"headers": headers}
    #either header means there is a body, and we need this later anyway
    hasbody = headers.get("Content-Length")
    if hasbody is None:
        return out
    body = splitheadbody[1]
    toread = int(hasbody) - len(body)
    while toread > 0:
        readin = conn.recv(1024)
        toread = toread - len(readin)
        body = body + readin
    out["body"] = body
    return out


#parse headers and return dictionary of headers
def parse_headers(headers):
    out = {}
    hdrlist = headers.split(bytes("\r\n", "utf-8"))
    #first handle request line
    reqline = hdrlist[0].split(bytes(" ", "utf-8"))
    out["request_type"] = reqline[0].decode("utf-8")
    out["path"] = reqline[1].decode("utf-8")
    out["http_type"] = reqline[2].decode("utf-8")
    for hdr in hdrlist[1:]:
        stuff = hdr.split(bytes(":", "utf-8"))
        #just in case so we don't have any data overwritten by naughty headers
        if stuff[0] == bytes("request_type", "utf-8") or stuff[0] == bytes("path", "utf-8") or stuff[0] == bytes("http_type", "utf-8"):
            continue
        #TODO: Handle headers with stuff like ; and multiple parts in them
        #Why is python string handling so terrible,
        #I thought is was the one thing python is
        #supposed to be good at. - Rob 3/15/22
        out[stuff[0].decode("utf-8")] = stuff[1].decode("utf-8").lstrip()
    if DEBUG:
        print("Parsed Headers: ", out)
        #This is here because docker doesn't like to flush output
        sys.stdout.flush()
    return out
