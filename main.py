import socketserver
from black import main
import webserver

#I use this for deciding when stuff gets printed
#I can move it if need be - Rob
DEBUG = True


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        webserver.handle_conn(self.request)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8000

    # Create the server, binding to localhost on port 8000
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Server started!", flush=True)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
