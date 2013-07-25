#!/usr/bin/python
'''
Created on 20.07.2013

@author: pycz
'''

import pty
from map import *
from random import randint
import sys, os, signal

class IO_discreptors:
    def __init__(self):
        self.stdin = None
        self.stdout = None

class Bot:
    def __init__(self, bot_path, num):
        self.bot_path = bot_path
        
        self.bot = IO_discreptors()
        
        self.bot_pid = None
        
        self.bot_pid, temp_fd = pty.fork()
        if self.bot_pid == 0:
            os.execl(self.bot_path, self.bot_path)
        
        self.bot.stdin = os.fdopen(temp_fd, "w", 0)
        self.bot.stdout = os.fdopen(temp_fd, "r", 0)
        
        self.name = self.readline()
        self.map = Map()
        self.num = num     # number of Bot
        
    def writeline(self, string):
        self.bot.stdin.write(string.strip() + "\n")
        self.bot.stdin.flush()
        self.bot.stdout.readline()  # pass not needed input 
        
    def readline(self):
        x = self.bot.stdout.readline().strip()
        return x
    
    def __del__(self):
        try:
            self.bot.stdin.close()
        except:
            pass
        try:
            self.bot.stdout.close()
        except:
            pass
        try:
            os.kill(self.bot_pid, signal.SIGKILL)
        except:
            pass

        
class Judge:

    def __init__(self, bot1_path, bot2_path):
        self.bot1_path = bot1_path
        self.bot2_path = bot2_path 
        
        self.wins = [0, 0]
        self.turn_pause = 0
        self.game_pause = 0
    
    def _go(self, bots):
        bot1coord = bots[0].readline()
        bots[1].writeline(bot1coord)
        bot2answ = bots[1].readline()
        bots[0].writeline(bot2answ)
        
        if bot2answ == "miss":
            bots[1].map.map[to_num_coord(bot1coord)[0]][to_num_coord(bot1coord)[1]].state = State.miss
        else:
            bots[1].map.map[to_num_coord(bot1coord)[0]][to_num_coord(bot1coord)[1]].state = State.kill
        
        if bots[0].map.map_losed():
            bots[0].writeline("lose")
            bots[1].writeline("win")
            return 1
        elif bots[1].map.map_losed():
            bots[0].writeline("win")
            bots[1].writeline("lose")
            return 0
        else:
            bots[0].writeline("nend")
            bots[1].writeline("nend")
            if bot2answ == "miss":
                return [bots[1], bots[0]]
            else:
                return bots
    
    def play_game(self):
        st1 = self.bot1.readline()
        st2 = self.bot2.readline()
        
        if st1 == "OK" and st2 == "OK":
            #can begin
            who_first = randint(0,1)
            self.bot1.writeline(str(who_first))
            self.bot2.writeline(str(1 - who_first))
            if who_first == 0:
                order = [self.bot1, self.bot2]
            else:
                order = [self.bot2, self.bot1]
            backup_order = order    
            while not (order == 0 or order == 1):
                backup_order = order
                order = self._go(order)
                
            return backup_order[order]  # winner!
        
        else:
            print "Bots are dont ready: B1 say %s ; B2 say %s \n" % st1, st2
        
    def play_championship(self, rounds):
        print "Begin\n"
        self.wins = [0, 0]
        for i in xrange(rounds):
            print "Round %d" % (i+1)
            self.bot1 = Bot(self.bot1_path, 0)
            self.bot2 = Bot(self.bot2_path, 1)
            winner = self.play_game()
            print "Win bot %d\n" % (winner.num + 1)
            self.wins[winner.num] += 1
        
        print 'Bot 1: %d \nBot 2: %d ' % (self.wins[0], self.wins[1])
        
if __name__ == '__main__':
    j = Judge("./bot.py", "./bot.py")
    j.play_championship(100)