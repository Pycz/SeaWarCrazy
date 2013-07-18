'''
Created on 11.07.2013

@author: pycz
'''
import sys
from random import randint

def to_num_coord(strCoord):    # return in tuple (letter, number)
    part1 = ord(strCoord[0]) - ord("a")
    if len(strCoord) == 2:
        part2 = int(strCoord[1]) - 1
    else:
        part2 = 9
    return (part1, part2)
        

class State:
    empty = 0
    kill = 1
    miss = 2
    ship = 3

class Cell:
    def __init__(self, state):
        self.state = state
        

class Map:
    def __init__(self):
        self.make_empty()
        
    def fill_with_ships(self):
        pass
        
    def make_empty(self):
        self.map = [[Cell(State.empty) for j in xrange(10)] for i in xrange(10)]
        
    def show_map(self):
        sys.stdout.write("  ")
        for i in xrange(10):
            sys.stdout.write(chr(ord('a')+i))
        sys.stdout.write('\n')
        for i in xrange(10):
            if i<9:
                sys.stdout.write(" ")
            sys.stdout.write(str(i+1))
            for j in xrange(10):
                state_now = self.map[j][i].state
                if state_now == State.empty:
                    cage = " "
                elif state_now == State.kill:
                    cage = "X"
                elif state_now == State.miss:
                    cage = "O"
                else:
                    cage = "#"
                
                sys.stdout.write(str(cage))
            sys.stdout.write('\n')
        
        

class Bot:
    pass


if __name__ == '__main__':
    Map().show_map()