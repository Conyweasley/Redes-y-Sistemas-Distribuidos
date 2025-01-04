# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import time
import os
import socket
from constants import *
from base64 import b64encode

#Funciones Modularizadas

def respuesta(code):
    return (str(code)+" "+str(error_messages[code])+str(EOL))

def validar_filename(FILENAME):
    # Checkea si el nombre es vacio.
    if(len(FILENAME)==0):
        return True
    # Si el filename no es vacio.
    s = set(FILENAME)
    check = s.difference(VALID_CHARS)
    # Checkea si existe algun caracter invalido en FILENAME
    return (len(check)==0)

def validar_int(str):
    s = set(str)
    check = s.difference(VALID_INT_ARG)
    return (len(check)==0)

def b64(r):
    r = b64encode(r)
    return r+b'\r\n'

class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.socket = socket
        self.directory = directory
        self.loop = True

    def send(self, message :str):
        self.socket.send(b""+message.encode("ascii"))
    
    def get_dir_path(self):
        current_wd = os.getcwd()
        current_wd = current_wd + "/" + self.directory
        return current_wd
    
    def create_dir(self):
        current_wd = os.getcwd()
        list = os.listdir(current_wd)
        for i in list:
            if i == self.directory:
                return
        os.mkdir(self.get_dir_path())
        #Seteo la flag en true para que no se cree el mismo archivo dos veces
        global DIRECTORIO_CREADO
        DIRECTORIO_CREADO = True

    def existe_filename(self, FILENAME:str):
        path = self.get_dir_path() + "/" + FILENAME
        check = os.path.isfile(path)
        return (check)

    def checkbarraN(self, c):
        if c.count(b'\n') > 0:
            self.send(respuesta(BAD_EOL))

    def check_args(self, arg_list):
        argc = len(arg_list)
        if((arg_list[0]=="quit" and argc == 1) or 
           (arg_list[0]=="get_file_listing" and argc == 1) or
           (arg_list[0]=="get_metadata" and argc == 2) or
           (arg_list[0]=="get_slice" and (argc == 4) and 
                                     validar_int(arg_list[2]) and 
                                     validar_int(arg_list[3]))):
            return True
        else:
            self.send(respuesta(INVALID_ARGUMENTS))    

    def receive_commands(self):
        client_disconnection = False
        buffer_overflow = False
        commands_list = []
        received_message = b''
        received_message_size = 0
        while True: 
            try:
                last_received_message = self.socket.recv(READ_SIZE)
            except:
                print("Desconexion del cliente inesperada")
                self.loop = False
                self.socket.close()
                break

            if last_received_message == b'':
                print("Desconexion del cliente inesperada")
                client_disconnection = True
                break

            received_message += last_received_message
            received_message_size += len(last_received_message)
            
            if received_message_size >= MAX_BUFFER:                
                buffer_overflow = True
                break

            if received_message.count(b'\r\n') > 0:
                commands_list = received_message.split(b'\r\n')
                commands_list = [comm for comm in commands_list if comm!=b'']
                break

        return client_disconnection, buffer_overflow, commands_list

    def handle(self):
        global DIRECTORIO_CREADO
        if not DIRECTORIO_CREADO:
            self.create_dir()

        (client_disconnection,
         buffer_overflow,
         commands_list,
        ) = self.receive_commands()

        if client_disconnection:
            self.loop = False
            self.socket.close()

            return

        if buffer_overflow:
            self.send(respuesta(BAD_REQUEST))
            self.loop = False
            self.socket.close()
            return

        self.execute_commands(commands_list)

    def execute_commands(self, commands_list):
        for command in commands_list:
            
            self.checkbarraN(command)
            command = command.decode("ascii")
            argv = command.split(" ")

            if (argv[0] == "quit"):
                if(self.check_args(argv)):
                    self.quit()
            #Comando GET_METADATA
            elif(argv[0] == "get_metadata"):
                if(self.check_args(argv)):
                    self.get_metadata(argv[1])
            #Comando GET_FILE_LISTING
            elif(argv[0] == "get_file_listing"):
                if(self.check_args(argv)):
                    self.get_file_listing()
            #Comando GET_SLICE
            elif(argv[0] == "get_slice"):
                if(self.check_args(argv)):
                    file = argv[1]
                    offset = argv[2]
                    size = argv[3]
                    self.get_slice(file, offset, size)
            #Comando caso contrario
            else:
                self.send(respuesta(INVALID_COMMAND))

    def quit(self):
        self.loop = False
        self.send(respuesta(CODE_OK))
        self.socket.close()
    
    def get_slice(self, FILENAME, OFFSET, SIZE):
        if(not validar_filename(FILENAME)):
            self.send(respuesta(INVALID_ARGUMENTS))

        elif(not self.existe_filename(FILENAME)):
            self.send(respuesta(FILE_NOT_FOUND))
        
        else:
            file_path = self.get_dir_path() + "/" + FILENAME
            file_size = os.path.getsize(file_path)
            OFFSET = int(OFFSET)
            SIZE = int(SIZE)
            #Chekeo de los argumentos 
            if(OFFSET < 0 or SIZE < 0):
                self.send(respuesta(INVALID_ARGUMENTS))
            
            elif(OFFSET > file_size):
                self.send(respuesta(BAD_OFFSET))
            
            elif(OFFSET + SIZE > file_size):
                self.send(respuesta(BAD_OFFSET))
            
            else:
                self.send(respuesta(CODE_OK))
                with open(file_path, 'rb') as file:
                    file.seek(OFFSET)
                    data = file.read(SIZE)
                    self.socket.send(b64(data))

    def get_metadata(self, FILENAME:str):
        if(not validar_filename(FILENAME)):
            self.send(respuesta(INVALID_ARGUMENTS))
        
        elif(not self.existe_filename(FILENAME)):
            self.send(respuesta(FILE_NOT_FOUND))
        
        else:
            file = self.get_dir_path() + "/" + FILENAME
            size = os.path.getsize(file)
            r = respuesta(CODE_OK)+str(size)+EOL
            self.send(r)

    def get_file_listing(self):
        try:
            list_of_files = os.listdir(self.get_dir_path())
        except:
            list_of_files = []
        r = respuesta(CODE_OK)
        if(len(list_of_files)!=0):
            for file in list_of_files:
                r = str(r) + f"{file}{EOL}"
            r+=EOL
        self.send(r)
