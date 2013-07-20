#!/usr/bin/python
'''
Created on 20.07.2013

@author: pycz
'''

from subprocess import PIPE, Popen
from map import *


class Judge:

    def __init__(self, bot1_path, bot2_path):
        self.bot1_path = bot1_path
        self.bot2_path = bot2_path 
        self.bot1 = Popen(self.bot1_path,
                          stdin  = PIPE,
                          stdout = PIPE, 
                          stderr = PIPE,
                          shell  = False)
        self.bot2 = Popen(self.bot2_path,
                          stdin  = PIPE,
                          stdout = PIPE, 
                          stderr = PIPE,
                          shell  = False)
        
        self.games_count = 0
        self.map1 = Map()
        self.map2 = Map()
    
    def play_game(self):
        pass
        
    
if __name__ == '__main__':
    pass