'''
Created on 20.07.2013

@author: pycz
'''

import sys
import random

def to_num_coord(str_coord):    # return in tuple (letter, number)
    part1 = ord(str_coord[0]) - ord("a")
    str_coord = str_coord.strip()
    if len(str_coord) == 2:
        part2 = int(str_coord[1]) - 1
    else:
        part2 = 9
    return (part1, part2)

def to_str_coord(tuple_coord):
    return chr(tuple_coord[0] + ord('a')) + str(tuple_coord[1] + 1)


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


    def get_rand_empty_coord(self):
        coords = []
        for i in xrange(10):
            for j in xrange(10):
                if self.map[i][j].state == State.empty:
                    coords.append((i,j))
        try:
            return random.choice(coords)
        except:
            return None

    def get_state_by_coords(self, i, j):
        return self.map[i][j].state


    def set_state_by_coords(self, i, j, st):
        self.map[i][j].state = st

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
                    cage = "-"
                else:
                    cage = "#"

                sys.stdout.write(str(cage))
            sys.stdout.write('\n')

    def map_beaten(self):  # have you a 1 non defeated ship?
        beaten = True
        for i in xrange(10):
            for j in xrange(10):
                if self.map[i][j].state == State.ship:
                    beaten = False
                    break
        return beaten

    def map_losed(self):  # all ships are detected and beaten?
        cages_biten = 4 + 3*2 + 2*3 + 4
        x = 0
        for i in xrange(10):
            for j in xrange(10):
                if self.map[i][j].state == State.kill:
                    x += 1

        if x >= cages_biten:
            return True
        else:
            return False
