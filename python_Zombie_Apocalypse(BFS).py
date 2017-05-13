#http://www.codeskulptor.org/#user40_JUgvA6FoHZaFrNs.py

"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[(self._grid_height * self._grid_width) for col in range(self._grid_width)] for row in range(self._grid_height)] 
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                visited.set_empty(row,col)
        boundary = poc_queue.Queue() 
        if entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        elif entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)        
        for cell in boundary:
            visited.set_full(cell[0],cell[1])
            distance_field[cell[0]][cell[1]] = 0
        
        while(len(boundary)):  
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0], cell[1])    
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
                    boundary.enqueue(neighbor)
        print distance_field
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        for human in self._human_list:
            mscore = 0
            newposition = (0,0)
            choice = self.eight_neighbors(human[0],human[1])
            move = False
            print choice
            for item in choice:
                if zombie_distance_field[item[0]][item[1]] != self._grid_height * self._grid_width and zombie_distance_field[item[0]][item[1]] > mscore:
                    #if self.is_empty(item[0], item[1]):
                    mscore = zombie_distance_field[item[0]][item[1]]
                    newposition = (item[0], item[1])
                    move = True
            if move is False:
                newposition = (human[0],human[1])
            new_human_list.append(newposition)        
        self._human_list = new_human_list 
        print self._human_list
            
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        #print self._zombie_list
        new_zombie_list = []
        for zombie in self._zombie_list:
            mscore = self._grid_height * self._grid_width
            newposition = (0,0)
            move = False
            choice = self.four_neighbors(zombie[0],zombie[1])
            print choice
            for item in choice:
                if human_distance_field[item[0]][item[1]] < mscore:
                    if self.is_empty(item[0], item[1]):
                        mscore = human_distance_field[item[0]][item[1]]
                        newposition = (item[0], item[1])
            if mscore < human_distance_field[zombie[0]][zombie[1]]:
                move = True
            if move is False:
                newposition = (zombie[0],zombie[1])            
            new_zombie_list.append(newposition)        
        self._zombie_list = new_zombie_list
        print self._zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Apocalypse(30, 40))


