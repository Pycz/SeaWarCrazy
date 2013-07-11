'''
Created on 11.07.2013

@author: pycz
'''

from random import randint

def to_num_coord(strCoord):
    part1 = ord(strCoord[0]) - ord("a")
    if len(strCoord) == 2:
        part2 = int(strCoord[1]) - 1
    else:
        part2 = 9
    return part1 + part2
        

class State:
    empty = 0
    kill = 1
    miss = 2

class Cell:
    def __init__(self, state):
        self.state = state
        

class Map:
    def __init__(self):
        self.make_empty()
        
    def fill_with_ships(self):
        pass
        
    def make_empty(self):
        m = [[Cell(State.empty) for j in xrange(10)] for i in xrange(10)]
        self.map = m

class Bot:
    pass


if __name__ == '__main__':
    pass