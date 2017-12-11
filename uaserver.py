#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


ERROR_405 = b"SIP/2.0 405 Method Not Allowed\r\n\r\n"
ERROR_400 = b"SIP/2.0 400 Bad Request\r\n\r\n"


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print(line.decode('utf-8'))
            METHOD = line.decode('utf-8').split(' ')[0]
            METHODS = ['INVITE', 'BYE', 'ACK']
            if line:
                sip = line.decode('utf-8').split(' ')[2]
                dos_puntos = str(line.decode('utf-8').split()[1].split())[5]
                arroba = str(line.decode('utf-8').split()[1].split())[14]
                if sip == 'SIP/2.0\r\n\r\n':
                    if METHOD == METHODS[0]:
                        self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                        self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif METHOD == METHODS[2]:
                        port = sys.argv[3]
                        aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 <' + port
                        os.system(aEjecutar)
                    elif METHOD == METHODS[1]:
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif METHOD != METHODS:
                        self.wfile.write(ERROR_405)
                elif dos_puntos != ':' or arroba != '@':
                    self.wfile.write(ERROR_400)
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos

    if len(sys.argv) < 4:
        sys.exit('Usage: python3 server.py IP port audio_file')
    serv = socketserver.UDPServer(('', int(sys.argv[2])), EchoHandler)
    if os.path.isfile(sys.argv[3]):
        print("Listening...")
serv.serve_forever()
