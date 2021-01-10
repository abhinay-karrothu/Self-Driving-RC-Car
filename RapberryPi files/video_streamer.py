import io
import socket
import struct
import time
import cv2
import numpy as np
import sys
from Driver import Driver
import pickle

server = '192.168.43.251'
#res = (320, 240)
#client_socket = socket.socket()
#client_socket.connect((server, 8000))
command_socket = socket.socket()
command_socket.connect((server, 9000))
recv_inst = True
drive = Driver()
#connection = client_socket.makefile('wb')
try:
    """output = SplitFrames(connection)
    with picamera.PiCamera(resolution=res, framerate=32) as camera:
        time.sleep(1)
        start = time.time()
        camera.start_recording(output, format = 'mjpeg')
        time.sleep(60)
        camera.stop_recording()
    connection.write(struct.pack('<L',0))"""
    while recv_inst:
        data = command_socket.recv(53)
        print(data)
        if data != b'':
            data = pickle.loads(data)
            print(data)
            if data == 'quit':
                recv_inst = False
            else:
                t = data['throttle']
                s = data['speed']
                a = data['angle']
                drive.drive(t,s,a)
        else:
            drive.drive(0,0,90)
    
finally:
    finish = time.time()
    #connection.close()
    #client_socket.close()
    command_socket.close()
    