# Self-Driving-RC-Car
Note: The Provided code is for Server and Client(Raspberry Pi) side code is in 'RaspberryPi Files' folder

https://github.com/abhinay-karrothu/Self-Driving-RC-Car/blob/master/images/unnamed-2.jpg

A RC car powered by a Neural Network which predicts the Steering angle in which car should drive based on the image input captured from the Camera.
RC car is modified using Raspberry pi, Camera, Driver module and Servo motor to act as a real time car. The Raspbery pi is connected to a server using VidGear API and python sockets to trasfer the camera data and driving commands.

# Libraried used:
1. Tensorflow 2.2.0 --> To Build and manage the Nueral Network
2. Sockets          --> To send Driving commands from Server to Client(Raspberry Pi)
3. VidGear API      --> To Send Camera Captured Image from Client to Server
4. Pygame           --> To Capture the Keyboard input on the fly, enables us to control the car using keyboard on the go.
5. OpenCV           --> To Preprocess the images
6. Numpy            --> To store the collected driving Data on the go (As Numpy is faster than Pandas)

# Files and their usage:
1. "Documentation": A Detailed Documetaion about the project is provided in the given PDF
2. "RaspberryPi files": Contains the Client side python files
   ---> Driver.py : This file converts the digital commands to electrical signals which is used to drive the car
   ---> client_module.py : This is the main file that runs all the required instance like camera, Driver.py file, establishing python sockets connection and makes the car ready to use
   ---> test_webcam.py: tests if the webcam is working or not
   ---> video_streamer.py: establishes the socket connection with the host and sends the video frames from client to the host/server.
   ---> video_streamer_API.py: works same as video_streamer but uses threads to make it run smooth.
3. "Behavioural Cloning.ipynb": Jupyter notebook that preprocess the driving data, builds the model and trains the model with better accuracy and saves the trained driving model.
4. "Traffic Sign Identifier.ipynb": Jupyter notebook that pre processes the traffic sign and signals images and trains the model and saves the trained signal identifier model.
5. "autonomous_mode.py": This file enables the car to drive autonomously using the trained neural network.
