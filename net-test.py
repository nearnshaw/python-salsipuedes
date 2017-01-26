#! /usr/bin/env python3

import locale
from dialog import Dialog   #ui
import socket                #UPD out
import socketserver          #TCP in


 

UDP_IP = "192.168.0.15"      # IP of PC
UDP_PORT = 7016              #  port in max
MESSAGE = "prueba superada"  # temporal, message to send
TCP_HOST = "192.168.0.17"    # IP de Raspberry Pi 
TCP_PORT =  9999             # Puerto en Raspberry Pi








# This is almost always a good thing to do at the beginning of your programs.
locale.setlocale(locale.LC_ALL, '')




# You may want to use 'autowidgetsize=True' here (requires pythondialog >= 3.1)
d = Dialog(dialog="dialog")
# Dialog.set_background_title() requires pythondialog 2.13 or later
d.set_background_title("My little program")




# In pythondialog 3.x, you can compare the return code to d.OK, Dialog.OK or
# "ok" (same object).
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








