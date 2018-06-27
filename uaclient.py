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
    Line = (LINE1 + USER + ":" + str(PORT) + ' ' + SIP + 'Expires:' + EXPIRES + "\r\n\r\n")
    my_socket.send(bytes(Line, 'utf-8'))

def invite():
    Line = (LINE2 + DIR + ' ' + SIP + 'Content-Type: application/sdp\r\n\r\n' +
            'v=0\r\no=' + USER + ' ' + SERVER + '\r\ns=misesion' +
            '\r\nt=0\r\nm=audio' + AUDIO_PORT + 'RTP' )
    my_socket.send(bytes(Line,'utf-8'))

def ack():
    Line = (LINE3 + DIR + SIP)
    my_socket.send(bytes(Line, "utf-8"))

def bye():
    Line = (LINE4 + DIR + SIP)
    my_socket.send(bytes(Line, "utf-8"))

def register_nonce(nonce):
    h = hashlib.sha1(bytes(PASSWD + "\n", "utf-8"))
    h.update(bytes(nonce, "utf-8"))
    digest = h.hexdigest()
    Line = ("REGISTER sip:" + USER + ":" + str(PORT) + " SIP/2.0\r\n" +
            "Expires: " + EXPIRES + "\r\n\r\n" +
            "Authorization: Digest response=" + digest +
            "\r\n\r\n")
    my_socket.send(bytes(Line, "utf-8"))

if __name__ == '__main__':
    parser = make_parser()
    cHandler = SmallSMILHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))

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
        DIR = LINE.split()[2]
        bye()

    print("Enviando:", LINE.split(' ')[1:])

    try:
        data = my_socket.recv(1024)
    except ConnectionRefusedError:
        sys.exit('Server is not listening')

    if data.decode('utf-8').split()[1] == '100':
        print('Recibido -- ', data.decode('utf-8'))
        my_socket.connect((PROXY_IP, int(PROXY_PORT)))
        ack()
        aEjecutar = ('./mp32rtp -i' + USER + '-p 23032 <' + AUDIO_PORT + " < " + FILE_AUDIO)
        os.system(aEjecutar)
        DATA = "Enviando fichero de audio."
        order = "cvlc rtp://@127.0.0.1:" + AUDIO_PORT
        os.system(order)
    elif data.decode('utf-8').split()[1] == '200':
        print('Recibido -- ', data.decode('utf-8'))
    elif data.decode('utf-8').split()[1] == '401':
        print('Recibido -- ', data.decode('utf-8'))
        my_socket.connect((PROXY_IP, int(PROXY_PORT)))
        register_nonce(data.decode('utf-8').split(' ')[2])
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))
    else:
        print(data.decode('utf-8'))
    print(data.decode('utf-8'))
print("Socket terminado.")
