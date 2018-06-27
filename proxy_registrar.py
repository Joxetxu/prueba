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

LINE1 = 'REGISTER sip:'
LINE2 = 'INVITE sip:'
LINE3 = 'ACK sip:'
LINE4 = 'BYE sip:'
SIP = 'SIP/2.0\r\n'

ERROR_405 = b"SIP/2.0 405 Method Not Allowed\r\n\r\n"
ERROR_400 = b"SIP/2.0 400 Bad Request\r\n\r\n"
ERROR_401 = b"SIP/2.0 401 Unauthorized\r\n"
ERROR_404 = b"SIP/2.0 404 User Not Found\r\n\r\n"


class SmallSMILHandler(ContentHandler):
    def __init__(self):
        self.list = {}
        self.Element = {'server': ['name', 'ip', 'port'],
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

        nonce = '89898347853'
        self.read_passwd()
        IP = self.clientaddress[0]
        PORT = DATA[1].split(':')[2]
        USER = DATA[1].split(':')[1]
        if user in self.users:
            EXPIRES = float(DATA[4]) + time.time()
            print(" ".join(DATA), "\r\n\r\n")
            self.users[user] = (IP, PORT,
                                    time.time(),
                                    EXPIRES)
            self.update_database()
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        else:
            if len(DATA) == 5:
                if int(DATA[4]) == 0:
                    try:
                        print("Usuario borrado:", user, "\r\n\r\n")
                        del self.users[user]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                        self.update_database()
                    except KeyError:
                        self.wfile.write(ERROR_404)
                elif int(DATA[4]) >= 0:
                    print(" ".join(DATA), "\r\n\r\n")
                    self.wfile.write(ERROR_401)
                    self.wfile.write(b"WWW-Authenticate:" + b'Digest nonce="' +
                                     bytes(nonce, "utf-8") +
                                     b'"')
                    self.wfile.write(b"\r\n\r\n")
            elif len(DATA) == 8:
                CLIENT = DATA[7].split("=")[1]
                EXPIRES = float(DATA[4]) + time.time()
                print(" ".join(DATA), "\r\n\r\n")
                if self.check_passwd(user, nonce) == CLIENT:
                    self.users[user] = (self.clientaddress[0],
                                            PORT,
                                            time.time(),
                                            EXPIRES)
                    self.update_database()
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                else:
                    self.wfile.write(ERROR_401)

    def invite(self, DATA):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            try:
                DIR = DATA[6].split("=")[1]
                IP= DATA[7]
                PORT = self.dicc_Data.get(_who_invites)[1]
                AUDIO_PORT = DATA[11]
                if DATA[1].split(":")[1] in self.users:
                    IP = self.dicc_Data.get(_to_send)[0]
                    PORT = self.dicc_Data.get(_to_send)[1]
                    my_socket.connect((IP, int(PORT)))
                    line = (LINE2 + _to_send + SIP +
                             "Content-Type: application/sdp\r\n\r\n" +
                             "v=0\r\no=" + DIR + " " + IP + "\r\ns=misesion" +
                             "\r\nt=0\r\nm=audio " + AUDIO_PORT + " RTP")
                    my_socket.send(bytes(line, "utf-8"))
                    print(line)
                    data = my_socket.recv(1024)
                    print(data.decode("utf-8"))
                    if Recieve[1] == "100":
                        self.wfile.write(data)
                else:
                    self.wfile.write(ERROR_404)
            except (TypeError, ConnectionRefusedError):
                self.wfile.write(ERROR_404)
    def ack(self, DATA):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            DIR = DATA[1].split(":")[1]
            IP = self.dicc_Data.get(_to_send)[0]
            PORT = self.dicc_Data.get(_to_send)[1]
            my_socket.connect((_to_send_ip, int(_to_send_port)))
            line = LINE3 + DIR + " SIP/2.0\r\n\r\n"
            my_socket.send(bytes(line, "utf-8"))
            print(line)

    def bye(self, DATA):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            DIR = DATA[1].split(':')[1]
            IP = self.dicc_Data.get(_to_send)[0]
            PORT = self.dicc_Data.get(_to_send)[1]
            my_socket.connect((IP, int(PORT)))
            line = (LINE4 + DIR + " SIP/2.0\r\n\r\n")
            my_socket.send(bytes(line, "utf-8"))
            print(line)
            data = my_socket.recv(1024)
            self.wfile.write(data)
            print(data.decode("utf-8"))
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.read_database()
        self.check_server()
        DATA = []
        if line:
            METHOD = line.decode('utf-8').split()[0]
            METHODS = ['INVITE', 'BYE', 'ACK', 'BYE']
            #debemos comprobar la peticion
            if METHOD == METHODS[0]:
                self.register(DATA)
            elif METHOD == METHODS[1]:
                self.invite(DATA)
            elif METHOD == METHODS[2]:
                self.ack(DATA)
            elif METHOD == METHODS[3]:
                self.bye(DATA)
            elif METHOD != METHODS:
                self.wfile.write(ERROR_405)
            else:
                self.wfile.write(ERROR_400)


if __name__ =='__main__':
    parser = make_parser()
    cHandler = SmallSMILHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))
    PORT = cHandler.list['serverport']
    DATABASE = cHandler.list['databasepath']
    PASSWD = cHandler.list['databasepasswdpath']
    SERVER = cHandler.list['serverport']
    serv = socketserver.UDPServer((SERVER, int(PORT)), SmallSMILHandler)
    try:
        print('Server ' + cHandler.list['servername'] +
              ' listening at port ' + str(PORT) + '...')
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor proxy")
