#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


if len(sys.argv) != 2:
    sys.exit('Usage: python3 uaserver.py config')

SERVER = '127.0.0.1'

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
                self.list[name + elemento] = attrs.get(elemento, "")

        def get_tags(self):
            return self.list


ERROR_405 = b"SIP/2.0 405 Method Not Allowed\r\n\r\n"
ERROR_400 = b"SIP/2.0 400 Bad Request\r\n\r\n"

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        line = self.rfile.read()
        print("El cliente nos manda ", line.decode('utf-8'))
        #logger
        if line:
            METHOD = line.decode('utf-8').split()[0]
            METHODS = ['INVITE', 'BYE', 'ACK']
            #debemos comprobar la peticion
            if METHOD == METHODS[0]:
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                self.wfile.write(b"SIP/2.0 200 OK\r\n")
            elif METHOD == METHODS[1]:
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            elif METHOD == METHODS[2]:
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 <' + La_Flaca.mp3
                os.system(aEjecutar)
            elif line.decode('utf-8').split()[1] != METHODS:
                self.wfile.write(ERROR_405)
            else:
                self.wfile.write(ERROR_400)
            print(line.decode('utf-8'))
        else:
            pass

if __name__ == "__main__":
    parser = make_parser()
    cHandler = SmallSMILHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    SERVER = cHandler.list['uaserverip']
    PORT = cHandler.list['uaserverport']
    PROXY_IP = cHandler.list['regproxyip']
    PROXY_PORT = cHandler.list['regproxyport']
    USER = cHandler.list['accountusername']
    AUDIO_PORT = cHandler.list['rtpaudioport']
    FILE_AUDIO = cHandler.list['audiopath']

    print(cHandler.list)
    serv = socketserver.UDPServer((SERVER,int(PORT)), EchoHandler)
    try:
        print("Listening...")
        serv.serve_forever()

    except KeyboardInterrupt:
        print("Finalizado servidor")
