from Driver import Driver
import cv2
import socket
from vidgear.gears import NetGear
import pickle
from threading import Thread
from time import sleep

host = '192.168.43.251'
video_port = '8000'
command_port = 8001

def steer():
    global command_client
    global driver
    global recv_inst
    try:
        while recv_inst:
            data = command_client.recv(53)
            if data is not None:
                data = pickle.loads(data)
                print(data)
                if data == b'quit':
                    recv_inst = False
                    driver.drive(0,0,90)
                    break
                else:
                    t = data['throttle']
                    s = data['speed']
                    a = data['angle']
                    driver.drive(t,s,a)
            else:
                driver.drive(0,0,90) 
        
    except:
        driver.drive(0,0,90)
        command_client.close()

def VideoStream():
    global command_client
    global driver
    global recv_inst
    print("Started")
    driver = Driver()
    recv_inst = True
    command_client = socket.socket()
    command_client.connect((host, command_port))
    Thread(target = steer).start()
    sleep(1)
    cam = cv2.VideoCapture(0)
    client = NetGear(address = host, port = video_port, protocol = 'tcp', pattern = 0, recieve_mode = False, logging = False)
    cam.set(3, 320)
    cam.set(4, 240)
    #cam.set(cv2.CAP_PROP_FPS, 10)
    while recv_inst:
        ret, frame = cam.read()
        if frame is None:
            break
        cv2.imshow("Car Cam", frame)
        client.send(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    client.close()
    command_client.close()
    cv2.destroyAllWindows()

Thread(target = VideoStream).start()
        