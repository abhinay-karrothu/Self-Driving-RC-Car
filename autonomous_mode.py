import socket
from vidgear.gears import NetGear
import pickle
from tensorflow.keras.models import load_model
from time import sleep
import cv2
import pygame
from pygame.locals import *
import numpy as np
import datetime 

def path_preprocess(img):
    img = img[0:300, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img = cv2.GaussianBlur(img, (3,3), 1)
    img = cv2.resize(img, (200,66))
    img = img/255
    return img 

def command_center():

    print('Started')
    global send_inst
    global image
    global command
    global command_connection
    global record
    throttle = 1
    angle = 90
    data = {'throttle':0, 'speed':0, 'angle':90}
    speed = 20
    model_path = "driver_test3.h5"
    model = load_model(model_path)
    pygame.init()
    pygame.display.set_mode((250, 250))
    send_inst = True
    start = False
    print("Thread Started")
    host = '192.168.43.251'
    command_port = 8001
    video_port = '8000'
    try:
        command_socket = socket.socket()
        command_socket.bind((host, command_port))
        command_socket.listen(0)
        command_connection, addr = command_socket.accept()
        print("Connected to", addr)
        print("Press 's' to start car\n Press 'w' to stop the car \n 1 - 50 \n 2 -  60 \n  3 - 70 \n 4 - 80\n Press 'q' to exit")
        sleep(0.5)
        server = NetGear(address=host, port=video_port, protocol='tcp', pattern=0, receive_mode= True)
        while send_inst:
            image = server.recv()
            cv2.imshow("Car View", image)
            if image is None:
                print("Image is none")
                break
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key_input = pygame.key.get_pressed()
                    if key_input[pygame.K_s]:
                        start = True
                    elif key_input[pygame.K_w]:
                        start = False
                    elif key_input[pygame.K_1]:
                        speed = 50
                    elif key_input[pygame.K_2]:
                        speed = 60
                    elif key_input[pygame.K_3]:
                        speed = 70
                    elif key_input[pygame.K_4]:
                        speed = 80
                    elif key_input[pygame.K_ESCAPE]:
                        break
            if start:  
                image = path_preprocess(image)
                image = np.array([image])
                angle = model.predict(image)[0][0]
                angle = int(angle)
                if angle < 0:
                    angle = 0
                if angle != data['angle'] or throttle != data['throttle']:
                    command = {'throttle':1, 'speed':20, 'angle':angle}
                    data['angle'] = angle
                    data['throttle'] = 1
                    print(command)
                    command = pickle.dumps(command)
                    command_connection.send(command)
    except:
        cv2.destroyAllWindows()
        server.close()
        command_socket.close()

if __name__ == '__main__':
    send_inst = True
    command = 'a'
    command_center()