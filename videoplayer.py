import os
import sys
from subprocess import Popen
import socketserver


movie1 = ("/media/pi/D09D-60B6/rickroll.mp4")
movie2 = ("/home/pi/Videos/movie2.mp4")
movie3 = ("/home/pi/Videos/movie1.mp4")
movie4 = ("/home/pi/Videos/movie2.mp4")

player = False


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
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-b', movie1])
        if str(self.data) == "b'kill'":
            os.system('killall omxplayer.bin')


if __name__ == "__main__":
    HOST, PORT = "192.168.0.17", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
