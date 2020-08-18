import numpy as np
file_name = "Data/driving_data.npz"
d = np.load(file_name)
a = d['images_paths']
b = d['angle']
c = d['throttle']
print(b)
print(c)
print(len(a))
print(len(b))