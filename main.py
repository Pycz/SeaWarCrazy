'''
Created on 11.07.2013

@author: pycz
'''
import sys
import random

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
        self.make_empty()
        grid = self.map
        self.make_empty()
        ship_len = 4
        while ship_len > 0:
            ship_count = 5 - ship_len  #how many ships of a kind are?
            for m in xrange(ship_count):
                possibilities = []
                # check horizontally
                b_i = 0
                b_j = 0
                e_i = ship_len-1
                e_j = 0
                while (e_i <= 9) and (e_j <= 9):
                    good = True
                    i = b_i
                    j = b_j
                    for n in xrange(ship_len):
                        good = good and (grid[i+n][j].state == State.empty)
                        if not good:
                            break
                    if good:
                        possibilities.append( ((b_i, b_j), (e_i, e_j)) )
                    
                    if e_i < 9:
                        b_i += 1
                        e_i += 1
                    else:
                        b_i = 0
                        b_j +=1
                        e_i = ship_len-1
                        e_j +=1          

                # check vertically
                b_i = 0
                b_j = 0
                e_i = 0
                e_j = ship_len-1
                while (e_i <= 9) and (e_j <= 9):
                    good = True
                    i = b_i
                    j = b_j
                    for n in xrange(ship_len):
                        good = good and (grid[i][j+n].state == State.empty)
                        if not good:
                            break
                    if good:
                        possibilities.append( ((b_i, b_j), (e_i, e_j)) )
                    
                    if e_j < 9:
                        b_j += 1
                        e_j += 1
                    else:
                        b_j = 0
                        b_i +=1
                        e_j = ship_len-1
                        e_i +=1                 
                
                # and pick a random position and place it
                pos = random.choice(possibilities)
                b_i = pos[0][0]
                b_j = pos[0][1]
                e_i = pos[1][0]
                e_j = pos[1][1] 
                while b_i <= e_i:
                    b_j = pos[0][1]
                    while b_j <= e_j:
                        self.map[b_i][b_j].state = State.ship
                        grid[b_i][b_j].state = State.ship
                        # where cant place
                        n_i = b_i - 1
                        while n_i <= b_i + 1:
                            n_j = b_j - 1
                            while n_j <= b_j + 1:
                                if (not(b_i == n_i and b_j == n_j) and 
                                        0 <= n_j <= 9 and
                                        0 <= n_i <= 9 and
                                        grid[n_i][n_j].state == State.empty):
                                    grid[n_i][n_j].state = State.miss
                                n_j += 1
                            n_i += 1
                        b_j += 1
                    b_i +=1
                # next ship done!
                #self.show_map()
            ship_len -= 1
            
            
            
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
    m = Map()
    m.fill_with_ships()
    m.show_map()