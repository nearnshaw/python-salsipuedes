import socketserver

from xbmcjson import XBMC, PLAYER_VIDEO
xbmc = XBMCJsonTransport("http://localhost/")
print(xbmc.JSONRPC.Ping())


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        if str(self.data) == "b'rickroll'":
            print("never gonna give you up")
            #self.request.sendall("never gonna give you up")
            # xbmc.executebuiltin('xbmc.PlayMedia("/media/pi/D09D-60B6","isdir")')
            # xbmc.PlayMedia("/media/pi/D09D-60B6","isdir")
            # xbmc.executebuiltin("Action(Fullscreen)")
            xbmc.Player.PlayPause([PLAYER_VIDEO])


if __name__ == "__main__":
    HOST, PORT = "192.168.0.17", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
