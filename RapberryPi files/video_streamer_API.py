from vidgear.gears import NetGear
import cv2
from Driver import Driver

host = '192.168.43.251'
port = '9001'

cam = cv2.VideoCapture(0)
options = {'bidirectional_mode': True}
client = NetGear(address = host, port = port, protocol = 'tcp', pattern = 1, receive_mode = False, logging = True, **options)
cam.set(3, 320)
cam.set(4, 240)
driver = Driver()
while True:
    ret, frame = cam.read()
    if frame is None:
        break
    cv2.imshow("Webcam", frame)
    data = client.send(frame)
    if data == "quit":
        driver.drive(0,0,90)
        break
    elif data != " ":
        t = data['throttle']
        s = data['speed']
        a = data['angle']
        driver.drive(t,s,a)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
client.close()
    