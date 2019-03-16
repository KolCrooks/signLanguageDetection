from DataProcessor import DataProc
from Model import ModelTrainer
import numpy as np
import Settings
<<<<<<< HEAD
import struct
import time
import socket
import sys
import _winapi as win32pipe
=======
>>>>>>> c597c4d27b7215d9191853772800f7006b657eb8


class Main:
    classes = ["Hello", "Dog", "Eat"]

    def __init__(self):
        # Load Model
        model_load = ModelTrainer()
        self.model = model_load.load_from_json("./model")
        self.data_process = DataProc(Settings)
<<<<<<< HEAD
        # Create a UDS socket


        # Connect the socket to the port where the server is listening
        server_address = r'\\.\pipe\SLPIPE'

        readHandle, writeHandle = win32pipe.CreatePipe(server_address)

        print('connecting to {}'.format(server_address))

        win32pipe

        while True:
            amount_expected = struct.unpack('I', sock.recv(4))[0]
            print("amount_expected :", amount_expected)

            message = sock.recv(amount_expected)
            print("Received message : ", message.decode())  # making it a string

            # Send data
            message_rev = message[::-1].decode()  # making it a string
            print("Sent message (reversed) : ", message_rev)

            sock.sendall(struct.pack('I', len(message_rev)) + message_rev.encode('utf-8'))

            time.sleep(2)

        # while True:
        #     self.listen()

    def listen(self):

            self.f.write(struct.pack('s', b'test'))  # Write str length and str
            self.f.seek(0)  # EDIT: This is also necessary
            print('Wrote')

            # n = struct.unpack('I', self.f.read(4))[0]  # Read str length
            # s = self.f.read(n)  # Read str
            # self.f.seek(0)  # Important!!!
            # print('Read:', s)

            time.sleep(10)
=======

        while True:
            self.listen()

    def listen(self):

>>>>>>> c597c4d27b7215d9191853772800f7006b657eb8


Main()