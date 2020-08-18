import numpy as np
file_name = "Data/driving_data.npz"
image_array = np.array([])
throttle_array = np.array([])
speed_array = np.array([])
angle_array = np.array([])
np.savez(file_name, images_paths = image_array, throttle = throttle_array, speed = speed_array, angle = angle_array)