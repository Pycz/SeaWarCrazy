#!/usr/bin/python
'''
Created on 11.07.2013

@author: pycz
'''
import sys
import random

from map import *


class Bot:
    def __init__(self, mode):
        self.my_map = Map()
        self.enemy_map = Map()
        self.my_map.fill_with_ships()
        self.strike_coord = None
        self.name = "Crazy Banana"
        self.graphic_mode = mode
        
    def is_my_ship_dead(self, num_coord):
        dead = True
        coords = [num_coord]
        passed = [num_coord]
        while dead and coords:
            num_coord = coords.pop()
            for i in [(num_coord[0] - 1, num_coord[1]),
                      (num_coord[0] + 1, num_coord[1]),
                      (num_coord[0], num_coord[1] - 1),
                      (num_coord[0], num_coord[1] + 1),
                     ]:
                if 0 <= i[0] <= 9 and 0 <= i[1] <= 9:
                    if self.my_map.map[i[0]][i[1]].state == State.ship:
                        dead = False
                        break
                    elif (self.my_map.map[i[0]][i[1]].state == State.kill) and (i not in passed):
                        coords.append(i)
                        passed.append(num_coord)
                        break
            
        return dead
        
    def get_coord_of_strike(self):
        self.strike_coord = self.enemy_map.get_rand_empty_coord()
        return to_str_coord(self.strike_coord) + "\n"
    
    def mark_result_of_strike(self, str_res):
        if str_res == "miss\n":
            state = State.miss
        elif str_res == "ou\n" or str_res == "kill\n":
            state = State.kill
        else:
            raise "Wrong massage on answer!"
        self.enemy_map.map[self.strike_coord[0]][self.strike_coord[1]].state = state
        
    def defense_enemy(self, str_coord):
        coord = to_num_coord(str_coord)
        if (self.my_map.map[coord[0]][coord[1]].state == State.empty or 
                                self.my_map.map[coord[0]][coord[1]].state == State.miss or
                                self.my_map.map[coord[0]][coord[1]].state == State.kill):
            message = "miss\n"
            if self.my_map.map[coord[0]][coord[1]].state == State.empty:
                self.my_map.map[coord[0]][coord[1]].state = State.miss
        else:
            if self.is_my_ship_dead(coord):
                message = "kill\n"
            else:
                message = "ou\n"
            self.my_map.map[coord[0]][coord[1]].state = State.kill
        return message

    def play(self):
        print self.name
        print "OK"
        if self.graphic_mode:
            self.my_map.show_map()
            self.enemy_map.show_map()        
        ######################
        self.first = int(sys.stdin.readline())
        res = "nend\n"
        self.turn = "my"
        if self.first == 1:  # im second
            answ = self.defense_enemy(sys.stdin.readline())
            sys.stdout.write(answ)
            if answ == "kill\n" or answ == "ou\n":
                self.turn = "him"
            res = sys.stdin.readline()
            if res == "win\n" or res == "lose\n":
                return None
            
        if self.graphic_mode:
            self.my_map.show_map()
            self.enemy_map.show_map()
                
        # there is my turn (or him, if hi kill or ou
        while res == "nend\n":
            if self.turn == "my":
                sys.stdout.write(self.get_coord_of_strike())
                answ = sys.stdin.readline()
                self.mark_result_of_strike(answ)
                if answ == "miss\n":
                    self.turn = "him"
            elif self.turn == "him":
                answ = self.defense_enemy(sys.stdin.readline())
                sys.stdout.write(answ)
                if answ == "miss\n":
                    self.turn = "my"
                    
            res = sys.stdin.readline()
            
            if self.graphic_mode:
                self.my_map.show_map()
                self.enemy_map.show_map()
                   
        return res
    

if __name__ == '__main__':
    graphic_mode = False
    if len(sys.argv) >= 2 and sys.argv[1] == "-g":
        graphic_mode = True
    b = Bot(graphic_mode)
    if graphic_mode:
        print b.play()
    else:
        b.play()
    