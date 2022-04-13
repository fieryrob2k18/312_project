import socket
from black import main
import webserver

#I use this for deciding when stuff gets printed
#I can move it if need be - Rob
DEBUG = True

def main():
    #TODO: Should I move all this to the webserver file
    #and just make one function call? - Rob
    soc = socket.socket()
    soc.bind(('0.0.0.0', 8000))

    #5 is "standard" connection # according to web tutorials
    soc.listen(5)

    while True:
        conn, addr = soc.accept()
        if DEBUG:
            print("New Connection from: ", addr, flush=True)
        webserver.handle_conn(conn)


if __name__ == "__main__":
    main()
