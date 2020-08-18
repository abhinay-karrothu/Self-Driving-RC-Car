import socket
from vidgear.gears import NetGear
import pickle
import pygame
from pygame.locals import *
from time import sleep
import cv2
import threading
import numpy as np
import datetime
#import lane_detector
            

def command_center(): #Main method
    
    print('Started')
    global send_inst
    global image
    global command
    global command_connection
    global record
    pressed_u = False
    pressed_b = False
    pressed_l = False
    pressed_r = False
    a = False
    b = False
    c = False
    d = False
    throttle = 0
    angle = 90
    data = {'throttle':0, 'speed':0, 'angle':90}
    done = 0
    speed = 50
    send_inst = True
    print("Thread Started")
    #initialize pygame which enables us to capture the keyboard key press
    pygame.init()
    pygame.display.set_mode((250, 250))
    #initialize the host ip address, port numbers of command and video communication
    host = '192.168.43.251'
    command_port = 8001
    video_port = '8000'
    try:
        #initialize command socket
        command_socket = socket.socket()     
        command_socket.bind((host, command_port))
        #listen to the connections until one is found
        command_socket.listen(0)
        command_connection, addr = command_socket.accept()
        print("Connected to", addr)
        sleep(0.5)
        #Initialize video socket using VIDGEAR package
        server = NetGear(address=host, port=video_port, protocol='tcp', pattern=0, receive_mode= True)
        while send_inst:
            image = server.recv()
            #image = lane_detector.detect_lanes(image)
            cv2.imshow("Car View", image)
            if image is None:
                print("Image is none")
                break
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key_input = pygame.key.get_pressed()
                    if key_input[pygame.K_a]:
                        speed = 20
                    if key_input[pygame.K_s]:
                        speed = 30
                    if key_input[pygame.K_d]:
                        speed = 40
                    if key_input[pygame.K_f]:
                        speed = 50
                    if key_input[pygame.K_UP]:
                        pressed_u = True
                        a = True       
                    if key_input[pygame.K_DOWN]:
                        pressed_b = True
                        b = True
                    if key_input[pygame.K_LEFT]:
                        pressed_l = True        
                        c = True
                    if key_input[pygame.K_RIGHT]:
                        pressed_r = True        
                        d = True
                    if key_input[pygame.K_ESCAPE]:
                        command = b'quit'
                        command_connection.send(command)
                        send_inst = False
                    if key_input[pygame.K_r]:
                        if record == 0:
                            print("Recording")
                            record = 1
                        elif record == 1:
                            record = 0
                            print("Stopped Recording")
                elif event.type == pygame.KEYUP:
                    if a and event.key == pygame.K_UP:
                        pressed_u = False
                        throttle = 0
                        a = False
                    if b and event.key == pygame.K_DOWN:
                        pressed_b = False
                        throttle = 0
                        b = False
                    if c and event.key == pygame.K_LEFT:
                        pressed_l = False
                        angle = 90
                        c = False
                    if d and event.key == pygame.K_RIGHT:
                        pressed_r = False
                        angle = 90
                        d = False    
            if pressed_u :
                throttle = 1
            if pressed_b :
                throttle = 2
            if pressed_l:
                if angle < 180:
                    angle += 10
                    sleep(0.1)
            if pressed_r:
                if angle > 0:
                    angle -= 10
                    sleep(0.1)
            if angle != data['angle'] or throttle != data['throttle']:
                command = {'throttle':throttle, 'speed':speed, 'angle':angle}
                data['angle'] = angle
                data['throttle'] = throttle
                print(command)
                command = pickle.dumps(command)
                command_connection.send(command)
            elif command == 'quit':
                command = b'quit'
                command_connection.send(command)
            if record == 1 and throttle == 1:
                image_name = str(datetime.datetime.now()).replace(" ", "_").replace(":", "_").replace(".","_")+".jpg"
                image_path = "Data/training_images/"+image_name
                cv2.imwrite(image_path, image)
                file_name = "Data/driving_data.npz"
                temp_data = np.load(file_name)
                image_array = temp_data['images_paths'].tolist()
                throttle_array = temp_data['throttle'].tolist()
                speed_array = temp_data['speed'].tolist()
                angle_array = temp_data['angle'].tolist()
                image_array.append(image_path)
                throttle_array.append(throttle)
                speed_array.append(90)
                angle_array.append(angle)
                image_array = np.array(image_array)
                throttle_array = np.array(throttle_array)
                speed_array = np.array(speed_array)
                angle_array = np.array(angle_array)
                np.savez(file_name, images_paths = image_array, throttle = throttle_array, speed = speed_array, angle = angle_array)
                

    except:
        cv2.destroyAllWindows()
        server.close()
        command_socket.close()

if __name__ == '__main__':
    send_inst = True
    command = 'a'
    record = 0
    command_center()