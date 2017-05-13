"""
Clone of 2048 game.
http://www.codeskulptor.org/#user40_dSvByRSsOh3253F.py
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def mov0end(lst):
    """
    Function that moves zeros to the end of a list.
    """
    newlist = []
    count = 0
    for number in range(len(lst)):
        if lst[number] == 0:
            newlist.append(lst[number])
        else:
            newlist.insert(count, lst[number])
            count += 1
    return newlist

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    newlist = mov0end(line)
    for number in range(len(newlist) - 1):
        if newlist[number] != 0 and newlist[number + 1] == newlist[number]:
            newlist[number] *= 2
            newlist[number + 1] = 0
    newlist = mov0end(newlist)        
    return newlist

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.newgrid = []
        self.reset()
        self.indD = {}                   
        self.indD[UP] = [(0, col) for col in range(self.grid_width)]
        self.indD[LEFT] = [(row, 0) for row in range(self.grid_height)]
        self.indD[DOWN] = [(self.grid_height - 1, col)for col in range(self.grid_width)]
        self.indD[RIGHT] = [(row, self.grid_width - 1)for row in range(self.grid_height)]
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """

        self.newgrid = [[0 for col in range(self.grid_width)] for row in range(self.grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """

        return ""

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        shift = False
        row = 0
        col = 0
        if direction < 3:
            atd = direction + 2
        else:
            atd = direction - 2
        temp = []
        for item in range(len(self.indD[direction])):
            for count in range(len(self.indD[atd])):
                row = self.indD[direction][item][0] + count * OFFSETS[direction][0]
                col = self.indD[direction][item][1] + count * OFFSETS[direction][1]
                temp.append(self.get_tile(row, col))
            temp = merge(temp)
            for count in range(len(temp)):
                row = self.indD[direction][item][0] + count * OFFSETS[direction][0]
                col = self.indD[direction][item][1] + count * OFFSETS[direction][1]
                #print 'row:', row, 'col:', col
                if self.newgrid[row][col] != temp[count]:
                    shift = True
                self.set_tile(row, col, temp[count])
            temp = []
        if shift == True:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        col = 0
        row = 0
        while row < self.grid_height and col < self.grid_width:
            row = random.randrange(0, self.grid_height)
            col = random.randrange(0, self.grid_width)
            #print 'row:', row, 'col:', col
            if self.newgrid[row][col] == 0:
                break
        self.newgrid[row][col] = random.choice([2,2,2,2,2,2,2,2,2,4])

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.newgrid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.newgrid[row][col]

    
poc_2048_gui.run_gui(TwentyFortyEight(5, 6))
