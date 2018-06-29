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
ERROR_401 = b"SIP/2.0 401 Unauthorized\r\n"

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}
    rtp = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        line = self.rfile.read()
        if line:
            METHOD = line.decode('utf-8').split()
            METHODS = ['INVITE', 'BYE', 'ACK']
            #debemos comprobar la peticion
            if METHOD[0] == METHODS[0]:
                self.rtp['1'] = METHOD[7].split("\r\n")[0], METHOD[11]
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                self.wfile.write(b"SIP/2.0 200 OK\r\n")
                self.wfile.write(SDP)
                #mi data es su message
                data = 'SIP/2.0 200 OK\r\n' + SDP.decode('utf-8')
            elif METHOD[0] == METHODS[1]:
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            elif METHOD[0] == METHODS[2]:
                aEjecutar = './mp32rtp -i' + self.rtp['1'][0] + '-p' + self.rtp['1'][0]
                aEjecutar += '<' + FILE_AUDIO
                os.system(aEjecutar)
            elif METHOD[0] != METHODS:
                self.wfile.write(ERROR_401)
            else:
                self.wfile.write("SIP/2.0 400 Method Not Allowed")
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
    FILE_LOG = cHandler.list['logpath']
    sdp = ('Content-Type: application/sdp\r\n\r\n' +
                'v=0\r\no=' + USER + ' ' + SERVER +
                '\r\ns=misesion' + '\r\nt=0\r\nm=audio ' +
                AUDIO_PORT + ' RTP')
    SDP = (bytes(sdp, 'utf-8'))
    serv = socketserver.UDPServer((SERVER,int(PORT)), EchoHandler)
    try:
        print("Listening...")
        serv.serve_forever()

    except KeyboardInterrupt:
        print("Finalizado servidor")
