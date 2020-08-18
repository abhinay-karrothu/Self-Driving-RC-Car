# Self-Driving-RC-Car
Note: The Provided code is for Server and Client(Raspberry Pi) side code will be provided soon

A RC car powered by a Neural Network which predicts the Steering angle in which car should drive based on the image input captured from the Camera.
RC car is modified using Raspberry pi, Camera, Driver module and Servo motor to act as a real time car. The Raspbery pi is connected to a server using VidGear API and python sockets to trasfer the camera data and driving commands.

# Libraried used:
1. Tensorflow 2.2.0 --> To Build and manage the Nueral Network
2. Sockets          --> To send Driving commands from Server to Client(Raspberry Pi)
3. VidGear API      --> To Send Camera Captured Image from Client to Server
4. Pygame           --> To Capture the Keyboard input on the fly, enables us to control the car using keyboard on the go.
5. OpenCV           --> To Preprocess the images
6. Numpy            --> To store the collected driving Data on the go (As Numpy is faster than Pandas)
