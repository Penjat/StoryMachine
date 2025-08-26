import numpy as np
from matplotlib import pyplot
import copy
from PIL import Image
from numpy import asarray

my_array = np.zeros((384,384))
my_array[:8,:] = 1
my_array[-8:,:] = 1
my_array[:,:8] = 1
my_array[:,-8:] = 1

pyplot.imshow(my_array)
pyplot.show()