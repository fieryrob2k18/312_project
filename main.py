import socket
from black import main

DEBUG = True

def main():
    soc = socket.socket()
    soc.bind('0.0.0.0', 8000)

    #5 is "standard" connection # according to web tutorials
    soc.listen(5)

    while True:
        conn, addr = soc.accept()
        if DEBUG:
            print("New Connection from: ", addr)
        handleConn(conn)

#Read request and send response
def handleConn(conn):
    return

#Read in header, process then handle body
def readReq(conn):
    stuff = conn.read(1024)
    while not("\r\n\r\n" in stuff):
        readin = conn.read(1024)
        stuff = stuff + readin
    if DEBUG:
        print("Request recieved: ", stuff)
    splitheadbody = stuff.split("\r\n\r\n", maxsplit=1)
    headers = parseHeaders(splitheadbody[0])
    return

#parse headers and return dictionary of headers
def parseHeaders(headers):
    out = {}
    hdrlist = headers.split("\r\n")
    #first handle request line
    reqline = hdrlist[0].split(" ")
    out["request_type"] = reqline[0]
    out["path"] = reqline[1]
    out["http_type"] = reqline[2]
    for hdr in hdrlist[1:]:
        stuff = hdr.split(":")
        #just in case so we don't have any data overwritten by naughty headers
        if stuff[0] == "request_type" or stuff[0] == "path" or stuff[0] == "http_type":
            continue
        #TODO: Handle headers with stuff like ; and multiple parts in them
        out[stuff[0]] = stuff[1].lstrip()
    return out

if __name__ == "__main__":
    main()
