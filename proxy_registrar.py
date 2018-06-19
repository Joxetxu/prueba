#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa proxy registrar
"""

import hashlib
import json
import socketserver
import socket
import sys
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler



class SmallSMILHandler(ContentHandler):
    def __init__(self):
        self.list = {}
        self.Element = {'server': ['name', 'ip', 'puerto'],
                        'database': ['path', 'passwdpath'],
                        'log': ['path']}

    def startElement(self, name, attrs):
        """
        Metodo para etiquetado de inicio"
        """
        if name in self.Element:
            for elemento in self.Element[name]:
                self.atr[elemento] = attrs.get(elemento, '')
                self.list.append(elemento.atr)
        def get_tags(self):
            return self.list

if __name__ =='__main__':
    parser = make_parser()
    cHandler = SmallSMILHandler()
    parser.setContentHandler(cHandler)
