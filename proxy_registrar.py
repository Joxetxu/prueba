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
                self.list[name + elemento] = attrs.get(elemento, "")
        def get_tags(self):
            return self.list

class ProxyRegisterHandler(socketserver.DatagramRequestHandler):
    users = {}
    passwds = {}

    def register2json(self):
        """me guarda el fichero en formato json"""
        with open(database, 'w') as file:
            json.dump(self.users, file)

    def json2registered(self):
        try:
            with open("register.json", "r") as file:
                json.load(self.users, file)

        except (NameError, FileNotFoundError, AttributeError):
            pass

    def chec_passwd(self, user, nonce):
        contra = self.passwd[user]
        h = hashlib.sha1(bytes(contra, "utf-8"))
        h.update(bytes(nonce, "utf-8"))
        return h.hexdigest()

    def time_expired(self):
        dicc = {}
        if self.users:
            for user in dicc:
                if dicc[user] < time.time():
                    del self.users[user]
            for user in self.users:
                dicc[user] = self.dicc[user][3]
            self.update_database()

    def read_passwd(self):

        with open(passwd_database, "r") as file:
            for line in data_file:
                key = line.split(" ")[0]
                value = line.split(" ")[1]
                self.passwdss[key] = value

    def register(self, DATA):

        nonce = '89898347853"
        self.read_passwd()




if __name__ =='__main__':
    parser = make_parser()
    cHandler = SmallSMILHandler()
    parser.setContentHandler(cHandler)
