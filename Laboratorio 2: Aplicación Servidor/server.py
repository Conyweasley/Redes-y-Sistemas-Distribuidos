#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import os
import optparse
import socket
import connection
import sys
from constants import *
import threading

class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
        print("Serving %s on %s:%s." % (directory, addr, port))
        # FALTA: Crear socket del servidor, configurarlo, asignarlo
        # a una dirección y puerto, etc.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creacion del socket
        self.sock.bind((addr, port)) # Se asigna a una direccion y puerto
        self.directory = directory
        # Sirve para reutilizar los puertos, cuando se cierran y abren muchos puertos.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threadControl = threading.BoundedSemaphore(10)

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        self.sock.listen(10) # Permite al server aceptar (1) conexiones,
        while True:
            # FALTA: Aceptar una conexión al server, crear una
            # Connection para la conexión y atenderla hasta que termine.
            client_socket, client_address = self.sock.accept()
            print(f"Conexion aceptada de: {client_address}")
            conn = connection.Connection(client_socket, self.directory)
            self.multi_client(conn)

    def multi_client(self, conn: connection):
        self.threadControl.acquire()
        def handler():
            try:
                while conn.loop:
                    conn.handle()
            finally:        
                self.threadControl.release()
        thread = threading.Thread(target= handler)
        thread.start()
            
def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()
