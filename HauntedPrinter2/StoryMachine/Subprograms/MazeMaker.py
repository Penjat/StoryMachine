from rx.subject import Subject
import numpy as np
import copy
from PIL import Image, ImageDraw, ImageFont
from numpy import asarray
import random
from matplotlib import pyplot


class MazeMaker:
    def __init__(self, display_output, printer_output):

        self.display_output = display_output
        self.printer_output = printer_output

        self.maze_array = np.zeros((1,1))

        self._maze_height = 50
        self._wall_size = 8.0
        
        self.current_selection = 0.0
        self.menu_items = ["wall size", "create maze", "set width", "set height", "main menu"]

        print("created a maze MazeMaker")


    def update_display(self):
        if self.selection == "set width":
            self.display_output.on_next(["MazeMaker", f"{self.selection} - {self.maze_width}"])
            return

        if self.selection == "set height":
            self.display_output.on_next(["MazeMaker", f"{self.selection} - {self.maze_height}"])
            return

        if self.selection == "wall size":
            self.display_output.on_next(["MazeMaker", f"{self.selection} - {self.wall_size}"])
            return
        
        self.display_output.on_next(["MazeMaker", f"{self.selection}"])


    @property
    def selection(self):
        return self.menu_items[int(self.current_selection)%len(self.menu_items)]

    @property
    def maze_width(self):
        return int(376.0/self.wall_size)

    # @maze_width.setter
    # def maze_width(self, value):
    #     self._maze_width = min(value, 360/self.maze_width)
    

    @property
    def maze_height(self):
        if self._maze_height % 2 == 0:
            return int(max(self._maze_height + 1, 11))
        
        return int(max(self._maze_height, 11))

    # @maze_height.setter
    # def maze_height(self, value):
    #     self._maze_height = value


    @property
    def wall_size(self):
        if self._maze_height % 2 == 0:
            return int(self._wall_size)
        return int(self._wall_size+1)

    # @wall_size.setter
    # def wall_size(self, value):
    #     self._wall_size = value
    
    

    # ----------- Maze Creation Methods -------------

    def print_maze(self):
        self.create_maze()
        self.expand_maze()
        self.printer_output.on_next(("print array", self.maze_array))

    def create_maze(self):
        self.maze_array = np.zeros((self.maze_height, self.maze_width))
        self.make_outer_walls()
        self.prims()  

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

    def prims(self, start = (2,0)):
        open_tiles = []

        # add rand tile to start
        open_tiles.append(start)
        print("starting prims")
        while len(open_tiles) != 0:
            tile = open_tiles[-1] # start at the last tile (recursive backtrace)
            # tile = random.choice(open_tiles) # start at a random tile prims
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
            
    # --------------- Processing Methods -----------------

    def expand_maze(self):
        self.maze_array = np.repeat(self.maze_array, self.wall_size, axis=1)
        self.maze_array = np.repeat(self.maze_array, self.wall_size, axis=0)
        print("done")

    def dijkstra(self):
        first_end, _ = self._dijkstra(self.maze_array, (1,1))
        self.maze_array[self.maze_array > 1] = 1
        second_end, length = self._dijkstra(self.maze_array, first_end)

        self.maze_array[first_end[0],first_end[1]] = length + 5
        self.maze_array[second_end[0],second_end[1]] = length + 5

        return first_end, second_end, length


    def _dijkstra(self, array, starting_pos):
        print("dijkstra...")
        open_cells = []
        open_cells.append(starting_pos)

        length = 2
        self.maze_array[starting_pos[0], starting_pos[1]] = length
        last_cell = starting_pos

        while len(open_cells) != 0:
            length += 1

            new_cells = []

            for position in open_cells:
                top = (position[0],position[1]-1)
                bottom = (position[0],position[1]+1)
                left = (position[0]-1,position[1])
                right = (position[0]+1,position[1])

                
                for cell in [top, bottom, left, right]:
                    if self.maze_array[cell[0], cell[1]] == 1:
                        self.maze_array[cell[0], cell[1]] = length
                        new_cells.append(cell)
                        last_cell = cell

            open_cells = new_cells


        return last_cell, length



    # --------------- Input Methods -----------------

    def process_right_knob(self, event):
        global current_selection
        if event == "up":
            self.current_selection += 0.5
        if event == "down":
            self.current_selection -= 0.5
        self.update_display()
    

    def process_left_knob(self, event):
        print("MazeMaker recieving right input")

        if self.selection == "set width":
            if event == "up":
                self._maze_width += 0.5
            if event == "down":
                self._maze_width = max(5, self._maze_width - 0.5)

        if self.selection == "set height":
            if event == "up":
                self._maze_height = min(46, self._maze_height + 0.5)
            if event == "down":
                self._maze_height = max(5, self._maze_height - 0.5)

        if self.selection == "wall size":
            if event == "up":
                self._wall_size = min(12, self._wall_size + 0.5)
            if event == "down":
                self._wall_size = max(1, self._wall_size - 0.5)
        self.update_display()

    def process_center_press(self, event):
        if event == "pressed":
            if self.selection == "main menu":
                self.printer_output.on_next(self.selection)
                return
            if self.selection == "create maze":
                self.print_maze()
                
            else:
                print(self.selection)

if __name__ == "__main__":
    print("Maze maker demo...")

    display_subject = Subject()
    printer_subject = Subject()

    display_subject.subscribe(lambda x: print(x))
    printer_subject.subscribe(lambda x: print(x))

    generator = MazeMaker(display_subject, printer_subject)
    generator.create_maze()
    maze_array, start, end = generator.dijkstra()
    generator.expand_maze()
    pyplot.imshow(generator.maze_array)
    pyplot.show()





