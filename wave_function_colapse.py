import numpy as np
import matplotlib.pyplot as plt


# Create a grid

possible_tiles = ['G', 'W', 'S']
width, height = 10, 10
num_tiles = len(possible_tiles)


grid = np.ones((height, width, num_tiles), dtype=bool)

print(grid)