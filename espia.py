#! /usr/bin/env python3

import threading
import locale
from dialog import Dialog   #ui
import socket                #UPD out
import socketserver          #TCP in
import pygame
#from _thread import start_new_thread

import signal
import time
from pirc522 import RFID

TCP_HOST = "192.168.0.19"    # IP de Raspberry Pi 
TCP_PORT =  9999             # Puerto en Raspberry Pi
UDP_IP = "192.168.0.15"      # IP of PC
UDP_PORT = 7016              #  port in max


MESSAGE = "aaa"  # temporal, message to send


#  manda OJO PP PW WIN


zapatofono = ("/home/pi/Documents/salsipuedes/audio/esp.wav") # ("/media/pi/D09D-60B6/esp.wav")
english = False
pasaporte = 123
password = 123

resolution = (640,480)
black = 0, 0, 0

retina = False
run = True
rdr = RFID()
util = rdr.util()
util.debug = True



pygame.init()
screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
pygame.mouse.set_visible(0)
# screen.fill(black)
pygame.mixer.init()
# zapato = pygame.mixer.Sound(zapatofono)
global playing


sockIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # TCP in
sockIn.bind((TCP_HOST, TCP_PORT))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP outt



pygame.display.set_mode(resolution)  #SACAR SACAAAR cuando ande




def rec_UDP():
    global retina # para poder usar variable localmente hay que decirle esto
    global TCP_HOST, TCP_PORT
    global zapatofono, zapato, english, pasaporte, password, sock
    
    while True:
        
        # UDP commands for listening

        data, addr = sockIn.recvfrom(1024)
        print ("received message:", data)
        if str(data) == "b'reset'":
            print("reset")
            zapato.stop()
            zapato.play()
            retina = False
            screen.fill(black)


        elif str(data) == "b'kill'":
            print("kill")
            zapato.stop()
            pygame.display.set_mode(resolution)


        elif str(data) == "b'test '":
            print("test")            
            sock.sendto(bytes("androcompu", "utf-8"), (UDP_IP, UDP_PORT))


        elif str(data) == "b'manual '":
            print("manual")            
            sock.sendto(bytes("retina manual", "utf-8"), (UDP_IP, UDP_PORT))
            retina = True

        elif str(data) == "b'reset '":
            print("reset")            
            sock.sendto(bytes("reset", "utf-8"), (UDP_IP, UDP_PORT))
            reset_all()



        elif str(data) == "":
            print("root")            
            sock.sendto(bytes("androcompu pasa audio zapatofono y pide passwords /reset /test /kill", "utf-8"), (UDP_IP, UDP_PORT))

        elif str(data) == "b'eng '":
            print("english")
            english = True
            zapatofono = ("/home/pi/Documents/salsipuedes/audio/eng.wav") #  ("/media/pi/D09D-60B6/eng.wav")
            zapato = pygame.mixer.Sound(zapatofono)
            sock.sendto(bytes("modo ingles", "utf-8"), (UDP_IP, UDP_PORT))


def reset_all():
    # para poder usar variable localmente hay que decirle esto
    global zapatofono, zapato, english, pasaporte, password, retina, playing, d

    english = False
    zapatofono = ("/home/pi/Documents/salsipuedes/audio/esp.wav") # ("/media/pi/D09D-60B6/esp.wav")    
    retina = False
    playing = False
    pygame.mixer.pause()
    zapato.stop()
    d.clear()               #dice metodo deprecated   http://pythondialog.sourceforge.net/doc/Dialog_class_overview.html#obsolete-methods
    print("did reset")


def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()

    
def play_audio():
    global zapato, zapatofono, playing
    zapato = pygame.mixer.Sound(zapatofono)
    pygame.mixer.unpause()
    while playing == True:
         zapato.play(loops = -1, fade_ms = 50)

def show_dialog():
    global zapatofono, zapato, english, pasaporte, password, retina, sock
    # You may want to use 'autowidgetsize=True' here (requires pythondialog >= 3.1)
    d = Dialog(dialog="dialog")
    # Dialog.set_background_title() requires pythondialog 2.13 or later
    d.set_background_title("Secrearia de Inteligencia Nacional")
    p = d.inputbox("Introduzca su Pasaporte")
    if str(p[1]) == str(pasaporte):     
        sock.sendto(bytes("PP", "utf-8"), (UDP_IP, UDP_PORT))
        pw = d.inputbox("Introduzca la Contraseña entregada telefonicamente")
        if str(pw[1]) == str(password):
            sock.sendto(bytes("PW", "utf-8"), (UDP_IP, UDP_PORT))
            men = d.menu("Bienvenido! Que desea hacer?:",
                    choices=[("(1)", "Consultar legajo"),
                             ("(2)", "Robar Chip")])
            if (str(men[1]) == "(2)"):
                d.msgbox("La clave es OMEGA")              
                sock.sendto(bytes("WIN", "utf-8"), (UDP_IP, UDP_PORT))
                
    

if __name__ == "__main__":
    global zapatofono, zapato, english, pasaporte, password, retina
    HOST, PORT = TCP_HOST, TCP_PORT

    # This is almost always a good thing to do at the beginning of your programs.
    locale.setlocale(locale.LC_ALL, '')

    listen_UDP = threading.Thread(target=rec_UDP)
    listen_UDP.start()


    # OLD
    # Create the server, binding to localhost on port 9999
    #server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    # sart_new_thread(server.serve_forever())
    #server.serve_forever()








signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    global zapatofono, zapato, english, pasaporte, password, retina, audio_player, playing
    
    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        retina = True
        playing = True       

        sock.sendto(bytes("OJO", "utf-8"), (UDP_IP, UDP_PORT))

        audio_player = threading.Thread(target=play_audio)
        audio_player.start()

        time.sleep(1)

        ask_user = threading.Thread(target=show_dialog)
        ask_user.start()

    #if retina == True:      
    #    print("RFID anduvo")
        
