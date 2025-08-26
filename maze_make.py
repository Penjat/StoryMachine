import numpy as np
from matplotlib import pyplot
import copy
from PIL import Image
from numpy import asarray
import random

class Maze:
	def __init__(self, width, height):
		self.maze_array = np.zeros((width,height))

	def make_outer_walls(self):
		self.maze_array[:1,:] = 1
		self.maze_array[:,:1] = 1
		self.maze_array[:,-1:] = 1
		self.maze_array[-1:,:] = 1

	def get_neighbors(self, position):
		top = (position[0],position[1]-2)
		bottom = (position[0],position[1]+2)
		left = (position[0]-2,position[1])
		right = (position[0]+2,position[1])

		output = []

		for x in (top,bottom,left,right):
			if self.get_val(x) == 0:
				output.append(x)

		return output

	def get_val(self, position):
		if position[0] < 0 or position[1] < 0 or position[0] >= self.maze_array.shape[0] or position[1] >= self.maze_array.shape[1]:
			return
		else:
			return self.maze_array[position[0],position[1]]
 
	def show(self):
		pyplot.imshow(self.maze_array)
		pyplot.show()

	def prims(self):
		open_tiles = []

		# add rand tile to start
		open_tiles.append((2,0))
		print("starting prims")
		while len(open_tiles) != 0:
			tile = open_tiles[-1] # start at the last tile (recursive backtrace)
			neighbors = self.get_neighbors(tile)

			# if it has neighbors, make a random connection
			if len(neighbors) != 0:
				link = random.choice(neighbors)

				self.maze_array[link[0],link[1]] = 1 # set to visited

				link_x = (link[0]-tile[0])/2 + tile[0]
				link_y = (link[1]-tile[1])/2 + tile[1]

				self.maze_array[int(link_x),int(link_y)] = 1 

				open_tiles.append(link)
			else:
				open_tiles.remove(tile)
			
		
		self.maze_array = np.repeat(self.maze_array, 4, axis=1)
		self.maze_array = np.repeat(self.maze_array, 4, axis=0)
		print("done")

# width = my_array.shape[0]
# height = my_array.shape[1]
maze = Maze(33,33)
maze.make_outer_walls()
maze.prims()
# print(maze.check_val((0,-1)))
# print(maze.get_neighbors((2,2)))
maze.show()
# for x in width:
# 	for y in height:
# 		print("hi")

# print(np.asarray(my_array == 1).nonzero())

