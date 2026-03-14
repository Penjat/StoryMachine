from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


img = Image.open('boat.JPG')

img_array = np.asarray(img)

noise = np.random.uniform(4872,5568)


array = np.mean(img_array, axis=2)

noise = np.random.uniform(-20, 20, array.shape)
array = array + noise
array[array <= 180] = 0
array[array > 180] = 1


plt.imshow(array)
plt.axis('off') 
plt.show()


print("hello butt face")