#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
# Dirección IP del servidor.
if len(sys.argv) < 3:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    LINE = sys.argv[1]
    my_socket.connect((SERVER, PORT))
    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE + ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))
