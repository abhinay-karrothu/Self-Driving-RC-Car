import cv2
import numpy as np
import socket
import pickle

host = '192.168.43.251'
port = 9001
video_socket = socket.socket()
video_socket.connect((host, port))

cam = cv2.VideoCapture(0)
cam.set(3, 320)
cam.set(4, 240)
while True:
    ret, frame = cam.read()
    cv2.imshow("Webcam", frame)
    img = pickle.dumps(frame)
    #print(len(img))
    video_socket.send(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()
video_socket.close()