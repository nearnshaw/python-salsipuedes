import os
import sys
import pygame
from subprocess import Popen
import socketserver
import psutil



movie1 = ("/media/pi/D09D-60B6/rickroll.mp4")
movie2 = ("/media/pi/D09D-60B6/testvideo1.mp4")
movie3 = ("/home/pi/Videos/movie1.mp4")
movie4 = ("/home/pi/Videos/movie2.mp4")

resolution = (640,480)

tvVolume = 45
#millibels = 2000.0 * log (10*(tvVolume))


player = False
FNULL = open(os.devnull,'w')
black = 0, 0, 0

pygame.init()
screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
pygame.mouse.set_visible(0)

def getplayers():
    procs = []
    for p in psutil.process_iter():
        if p.name() == 'omxplayer.bin':
            procs.append(p)
    return procs

def killoldplayers(procs):
    for p in procs:
        p.kill()

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """




    def handle(self):

        
        screen.fill(black)

        players = getplayers()
        n = 0

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        n += 1
        if n == 10:
            n = 0
        

        if str(self.data) == "b'rickroll'":
            print("never gonna give you up")
            # vol at 50%, in theory both aux and hdmi
            cmd = "omxplayer -b -o both --vol -602 --layer %d %s "%(n,movie1)
            Popen(cmd, shell=True, stdout=FNULL,stderr=FNULL)
            killoldplayers(players)
        elif str(self.data) == "b'test1'":
            print("video 2")
            cmd = "omxplayer -b -o both --vol -602  --layer %d %s "%(n,movie2)
            Popen(cmd, shell=True, stdout=FNULL,stderr=FNULL)
            killoldplayers(players)

        elif str(self.data) == "b'reset'":
            print("reset")
            killoldplayers(getplayers())
            screen.fill(black)


        elif str(self.data) == "b'kill'":
            print("kill")
            killoldplayers(getplayers())
            pygame.display.set_mode(resolution)


        elif str(self.data) == "b'test'":
            print("test")            

        elif str(self.data) == null:
            print("root")            
            


if __name__ == "__main__":
    HOST, PORT = "192.168.0.17", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
