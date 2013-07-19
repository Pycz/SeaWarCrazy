'''
Created on 11.07.2013

@author: pycz
'''
import sys
import random

def to_num_coord(str_coord):    # return in tuple (letter, number)
    part1 = ord(str_coord[0]) - ord("a")
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
    def __init__(self):
        self.my_map = Map()
        self.enemy_map = Map()
        self.my_map.fill_with_ships()
        self.strike_coord = None
        
    def get_coord_of_strike(self):
        self.strike_coord = self.enemy_map.get_rand_empty_coord()
        return to_str_coord(self.strike_coord)
    
    def mark_result_of_strike(self, state_res):
        self.enemy_map[self.strike_coord[0]][self.strike_coord[1]].state = state_res
        
    def defense_enemy(self, str_coord):
        coord = to_num_coord(str_coord)
        if (self.my_map[coord[0]][coord[1]].state == State.empty or 
                                self.my_map[coord[0]][coord[1]].state == State.miss or
                                self.my_map[coord[0]][coord[1]].state == State.kill):
            message = "miss\n"
        else:
            pass
        
    def is_my_ship_dead(self, num_coord):
        dead = True
        coords = [num_coord]
        passed = [num_coord]
        while dead or coords:
            num_coord = coords.pop()
            for i in [(num_coord[0] - 1, num_coord[0]),
                      (num_coord[0] + 1, num_coord[0]),
                      (num_coord[0], num_coord[0] - 1),
                      (num_coord[0], num_coord[0] + 1),
                     ]:
                if self.my_map[i[0]][i[1]].state == State.ship:
                    dead = False
                    break
                elif (self.my_map[i[0]][i[1]].state == State.kill) and (i not in passed):
                    coords.append(i)
                    passed.append(num_coord)
                    break
            
        return dead

if __name__ == '__main__':
    m = Map()
    m.fill_with_ships()
    m.show_map()