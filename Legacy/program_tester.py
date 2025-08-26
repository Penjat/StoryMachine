
from rx.subject import Subject

# Maze maker
from MazeMaker import *
from matplotlib import pyplot
from numpy import asarray
import math

#  Tarot Reader
from TarotReader import *
import os
from PIL import Image, ImageOps
import numpy as np
from random import randint
import random

# Alt Tarot
from AltTarot import *
import os
import openai
import json
import requests

# LiveALive
from LiveALive import *
import re


maker = MazeMaker(None, None)
# maker.create_maze()
maker.maze_array = np.zeros((101, 101))

import numpy as np


# Example usage
width = 20
height = 20
grid_size = 10

# maker.maze_array[5:5+height, 5:5+width] = 1
# maker.make_outer_walls()
# maker.prims()

# pyplot.imshow(maker.maze_array)
# pyplot.show()


load_img_rz = Image.open("/Users/spencersymington/Documents/SCS-joystickbold.png").convert("RGBA").resize((int(762/6),int(399/6)))
maker.maze_array = asarray(load_img_rz)

# maker.maze_array = data
inverter = lambda x: 1-x

maker.maze_array = np.where(maker.maze_array[:, :, 3] == 255, 1, 0)
maker.maze_array = inverter(maker.maze_array)

# maker.prims((30,10))
# maker.prims((50,70))
# maker.prims((30,138))

# maker.prims()
maker.prims((4,18))
maker.prims((6,64))
maker.prims((6,106))
# maker.prims((3,182))
# maker.prims((96,182))
# maker.maze_array = inverter(maker.maze_array)
pyplot.imshow(maker.maze_array)
# pyplot.imshow(maker.maze_array)
pyplot.show()
# reader = TarotReader(None, None)
# card = reader.tarot_reading()

# pyplot.imshow(maker.maze_array)
# pyplot.show()


# alt_tarot_reader = AltTarot(None, None)
# data = alt_tarot_reader.tarot_reading()
# print(data)
# pyplot.imshow(data[2])
# pyplot.show()


# display_output = Subject()
# printer_output = Subject()

# game = LiveALive(display_output, printer_output)
# game.start_story()



# while game.is_playing:
# 	print(f"TEXT SO FAR:{game.text_so_far}")
# 	user_input = input("")
# 	game.process_choice(user_input)




print("exiting loop...")

