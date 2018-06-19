#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys
import json
import time
import os
import hashlib
from xml.sax import make_parser
from xml.sax.handler import ContentHandler



try:
    if len(sys.argv)<3:
        sys.exit('Usage: python uaclient.py config method option')
except IndexError:
    sys.exit('Usage: python uaclient.py config method option')

LINE1 = 'REGISTER sip:'
LINE2 = 'INVITE sip:'
LINE3 = 'ACK sip:'
LINE4 = 'BYE sip:'
SIP = 'SIP/2.0\r\n'


class SmallSMILHandler(ContentHandler):
    """
        Clase para manejar SmallSMILHandler
    """
    def __init__(self):
        self.list = {}
        self.Element = {"account": ["username", "passwd"],
                         "uaserver": ["ip", "port"],
                         "rtpaudio": ["port"],
                         "regproxy": ["ip", "port"],
                         "log": ["path"],
                         "audio": ["path"]}

    def startElement(self, name, attrs):
        """
        Metodo para etiquetado de inicio"
        """
        if name in self.Element:
            for elemento in self.Element[name]:
                self.list[name + elemento] = attrs.get(elemento, '')
        def get_tags(self):
            return self.list

def register():
    """
    Cuando quiero registrarme en el proxy
    """
    DATA = (LINE1 + USER + ":" + str(PORT) + ' ' + SIP + 'Expires:' + EXPIRES + "\r\n\r\n")
    my_socket.send(bytes(DATA, 'utf-8'))
    #logger.action_send(Proxy_Ip, Proxy_Port, DATA)

def invite():
    DATA = (LINE2 + DIR + ' ' + SIP + "Content-Type: application/sdp\r\n\r\n" +
            "v=0\r\no=" + User_Name + " " + SERVER + "\r\ns=misesion" +
            "\r\nt=0\r\nm=audio " + 'Audio_Puerto' + "RTP")
    my_socket.send(bytes(DATA,'utf-8'))
    #logger.action_send(Proxy_Ip, Proxy_Port, DATA)

def ack():
    DATA = (LINE3 + DIR + SIP)
    my_socket.send(bytes(DATA, "utf-8"))
    #logger.action_send(Proxy_Ip, Proxy_Port, DATA)

def bye():
    DATA = (LINE4 + DIR + SIP)
    my_socket.send(bytes(DATA, "utf-8"))
    #logger.action_send(Proxy_Ip, Proxy_Port, DATA)

if __name__ == '__main__':
    parser = make_parser()
    cHandler = SmallSMILHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))

    print(cHandler.list)

# Constantes. Dirección IP del servidor y contenido a enviar
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    LINE = sys.argv[1] + ' ' + ''.join(sys.argv[2]+' ' + ''.join(sys.argv[3]))
    METHOD = sys.argv[2]
    METHODS = ['REGISTER', 'INVITE', 'ACK', 'BYE']
    SERVER = cHandler.list['uaserverip']
    PORT = cHandler.list['uaserverport']
    USER = cHandler.list['accountusername']
    PASSWD = cHandler.list['accountpasswd']
    PROXY_IP = cHandler.list['regproxyip']
    PROXY_PORT = cHandler.list['regproxyport']
    AUDIO_PORT = cHandler.list['rtpaudioport']
    FILE_AUDIO = cHandler.list['audiopath']

#Meto el if porque dependiendo de INVITE, BYE o REGISTR Meto
#tiempo de expieracion o direccion
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, int(PORT)))
    if METHOD == METHODS[0]:
        Invitation = PROXY_IP
        EXPIRES = LINE.split()[2]
        register()
    elif METHOD == METHODS[1]:
        DIR = LINE.split()[2]
        invite()
    elif METHOD == METHODS[3]:
        #Tengo que declarar la variable user_to_send pero no se que es
        DIR = LINE.split()[2]
        bye()

    print("Enviando:", '')

    try:
        data = my_socket.recv(1024)
        recibido = data.decode('utf-8').split()
        print('Recibido -- ', data.decode('utf-8'))
    except ConnectionRefusedError:
        sys.exit('Server is not listening')

    if data.decode('utf-8').split()[1] == '100':
        print('x')
    elif data.decode('utf-8').split()[1] == '200':
        print('y')
    elif data.decode('utf-8').split()[1] == '401':
        print('z')
    else:
        print(data.decode('utf-8'))
print("Socket terminado.")
