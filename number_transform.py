import numpy as np
from matplotlib import pyplot
import copy
from PIL import Image
from numpy import asarray
import math

# want to converty a 3D array into a 2D array
print("starting number transform...")
my_array = np.array([[[200,300,100],[200,300,100],[200,200,100],[200,300,100]],[[200,120,100],[200,105,100],[200,300,100],[200,300,100]],[[200,300,100],[200,300,100],[200,300,100],[200,300,100]],[[200,300,100],[200,300,100],[200,300,100],[200,300,100]]])

my_array = np.compress([True, True, True], my_array, axis=2)

load_img_rz = Image.open('my_pic.jpg').convert('1')

# data = asarray(load_img_rz)



# data = np.compress([False, False, True], data, axis=2)

new_array = np.ones((6,9))

# output_array = new_array.reshape(-1,8)
width_padding = (math.ceil(new_array.shape[1]/8) * 8) - new_array.shape[1]
print(width_padding)
new_array = np.pad(new_array, [(0, 0), (0, width_padding)], mode='constant')

print(math.ceil(new_array.shape[0]/8))
print(new_array.shape)

pyplot.imshow(new_array)
pyplot.show()

# width = my_array.shape[0]
# height = my_array.shape[1]

# convert a bit into a hex
# print(my_array)
# print("--------")
# print(my_array[:,:1])

def convert_byte(byte):
	i = 1
	val = 0
	for bit in byte:
		if bit > 100:
			val += i
		i = i*2	
	return val


# byte = [222,10,200,200,102,150,220,200]

# print(convert_byte(byte))
# # want to convert that array into a list of hex numbers

# my_array = my_array.reshape(-1,8)
# print(my_array)

# for 

# byte_array = applyall(my_array)

# print(byte_array)

# print("done.")
