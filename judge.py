#!/usr/bin/python
'''
Created on 20.07.2013

@author: pycz
'''

from subprocess import PIPE, Popen
from map import *
from random import randint

class Bot:
    def __init__(self, bot_path, num):
        self.bot_path = bot_path
        self.bot = Popen(self.bot_path,
                          stdin  = PIPE,
                          stdout = PIPE, 
                          stderr = PIPE,
                          shell  = False)
        
        self.name = self.readline()
        self.map = Map()
        self.num = num
        
    def writeline(self, string):
        self.bot.stdin.write(string.strip() + "\n")
        
    def readline(self):
        return self.bot.stdout.readline().strip()
        
class Judge:

    def __init__(self, bot1_path, bot2_path):
        self.bot1_path = bot1_path
        self.bot2_path = bot2_path 
        
        self.bot1 = Bot(self.bot1_path, 0)
        self.bot2 = Bot(self.bot2_path, 1)
        
        self.games_count = 0
        self.turn_pause = 0
        self.game_pause = 0
    
    def _go(self, *bots):
        bot1coord = bots[0].readline()
        self.bots[1].writeline(bot1coord)
        bot2answ = self.bots[1].readline()
        self.bots[0].writeline(bot2answ)
        
        if bot2answ == "miss":
            self.bots[1].map.map[to_num_coord(bot1coord)[0]][to_num_coord(bot1coord)[1]] = State.miss
        else:
            self.bots[1].map.map[to_num_coord(bot1coord)[0]][to_num_coord(bot1coord)[1]] = State.kill
        
        if self.bots[0].map.map_losed():
            self.bots[0].writeline("lose")
            self.bots[1].writeline("win")
            return 1
        elif self.bots[1].map.map_losed():
            self.bots[0].writeline("win")
            self.bots[1].writeline("lose")
            return 0
        else:
            self.bots[0].writeline("nend")
            self.bots[1].writeline("nend")
            if bot2answ == "miss":
                return [bots[1], bots[0]]
            else:
                return bots
    
    def play_game(self):
        st1 = self.bot1.readline()
        st2 = self.bot2.readline()
        
        if st1 == "OK" and st2 == "OK":
            #can begin
            who_first = randint(1)
            self.bot1.writeline(str(who_first))
            self.bot2.writeline(str(1 - who_first))
            if who_first == 0:
                order = [self.bot1, self.bot2]
            else:
                order = [self.bot2, self.bot1]
            backup_order = order    
            while order != 0 or order != 1:
                backup_order = order
                order = self._go(order)
                
            return backup_order[order]  # winner!
        
        else:
            print "Bots are dont ready: B1 say %s ; B2 say %s \n" % st1, st2
        
    
if __name__ == '__main__':
    pass