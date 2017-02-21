#! /usr/bin/env python3

import locale
from dialog import Dialog   #ui
import socket                #UPD out
import socketserver          #TCP in
import pygame
from _thread import start_new_thread


UDP_IP = "192.168.0.15"      # IP of PC
UDP_PORT = 7016              #  port in max
MESSAGE = "prueba superada"  # temporal, message to send
TCP_HOST = "192.168.0.19"    # IP de Raspberry Pi 
TCP_PORT =  9999             # Puerto en Raspberry Pi

zapatofono = ("/media/pi/D09D-60B6/japanese.wav")


resolution = (640,480)
black = 0, 0, 0

pygame.init()
screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
pygame.mouse.set_visible(0)
# screen.fill(black)
pygame.mixer.init()
zapato = pygame.mixer.Sound(zapatofono)


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


        if str(self.data) == "b'reset'":
            print("reset")
            zapato.stop()
            zapato.play()
            screen.fill(black)


        elif str(self.data) == "b'kill'":
            print("kill")
            zapato.stop()
            pygame.display.set_mode(resolution)


        elif str(self.data) == "b'test'":
            print("test")            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            sock.sendto(bytes("androcompu", "utf-8"), (UDP_IP, UDP_PORT))

        elif str(self.data) == null:
            print("root")            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            sock.sendto(bytes(MESSAGE, "androcompu pasa audio zapatofono y pide passwords /reset /test /kill"), (UDP_IP, UDP_PORT))


if __name__ == "__main__":
    HOST, PORT = TCP_HOST, TCP_PORT

    # This is almost always a good thing to do at the beginning of your programs.
    locale.setlocale(locale.LC_ALL, '')


    zapato.play(loops = -1, fade_ms = 50)


    # You may want to use 'autowidgetsize=True' here (requires pythondialog >= 3.1)
    d = Dialog(dialog="dialog" , autowidgetsize=True)
    # Dialog.set_background_title() requires pythondialog 2.13 or later
    d.set_background_title("My little program")

    # In pythondialog 3.x, you can compare the return code to d.OK, Dialog.OK or
    # "ok" (same object).

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    # sart_new_thread(server.serve_forever())
    server.serve_forever()

    print("haciendo otras cosas too")

    if d.yesno("Presione OK para ganar") == d.OK:
        d.msgbox("You have been warned...")

        # 'tags' now contains a list of the toppings chosen by the user
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        pass
    else:
        code, tag = d.menu("OK, then you have two options:",
                           choices=[("(1)", "Leave this fascinating example"),
                                    ("(2)", "Leave this fascinating example")])
        if code == d.OK:
            # 'tag' is now either "(1)" or "(2)"
            pass



