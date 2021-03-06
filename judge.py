#!/usr/bin/python
'''
Created on 20.07.2013

@author: pycz
'''

import pty
import time
import re

from threading import Lock
from map import *
from random import randint
import os
import signal

jar_re = re.compile(r".*\.jar$")


class IO_discreptors:
    def __init__(self):
        self.stdin = None
        self.stdout = None


class Bot:
    def __init__(self, bot_path, num):
        # java jar support
        if jar_re.match(bot_path):
            bot_path = "java -jar " + bot_path

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

    def get_map(self):
        return self.map


class Judge:

    def __init__(self, bot1_path, bot2_path, turn_pause=0, game_pause=0, lock=Lock(), alive=[True, ]):
        self.bot1_path = bot1_path
        self.bot2_path = bot2_path

        self.alive = alive
        self.lock = lock
        self.wins = [0, 0]
        self.turn_pause = turn_pause
        self.game_pause = game_pause
        self.bot1 = None
        self.bot2 = None
        try:
            self.bot1 = Bot(self.bot1_path, 0)
            self.bot2 = Bot(self.bot2_path, 1)
        except:
            raise

    def _go(self, bots):
        bot1coord = bots[0].readline()
        bots[1].writeline(bot1coord)
        bot2answ = bots[1].readline()
        bots[0].writeline(bot2answ)

        self.lock.acquire()
        if bot2answ == "miss":
            bots[1].map.map[to_num_coord(bot1coord)[0]][to_num_coord(bot1coord)[1]].state = State.miss
        else:
            bots[1].map.map[to_num_coord(bot1coord)[0]][to_num_coord(bot1coord)[1]].state = State.kill
        self.lock.release()

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
            # can begin
            who_first = randint(0, 1)
            self.bot1.writeline(str(who_first))
            self.bot2.writeline(str(1 - who_first))
            if who_first == 0:
                order = [self.bot1, self.bot2]
            else:
                order = [self.bot2, self.bot1]
            backup_order = order
            while not (order == 0 or order == 1):
                if self.alive[0]:
                    backup_order = order

                    order = self._go(order)

                    time.sleep(self.turn_pause)
                else:
                    raise Exception("End of thread")

            return backup_order[order]  # winner!

        else:
            print "Bots are dont ready: B1 say %s ; B2 say %s \n" % (st1, st2)

    def play_championship(self, rounds, maplist=[None, None, 0], winlist=[None, None, 0]):  # kostili
        print "Begin\n"

        self.lock.acquire()
        self.wins = [0, 0]
        winlist[0] = self.wins[0]
        winlist[1] = self.wins[1]
        winlist[2] = 0
        self.lock.release()

        time.sleep(self.game_pause)
        for i in xrange(rounds):
            if self.alive[0]:
                print "Round %d" % (i + 1)

                self.lock.acquire()
                self.bot1 = Bot(self.bot1_path, 0)
                self.bot2 = Bot(self.bot2_path, 1)
                maplist[0] = self.bot1.get_map()
                maplist[1] = self.bot2.get_map()
                maplist[2] += 1
                self.lock.release()

                winner = self.play_game()
                if winner:
                    print self.bot1.name + " (" + str(self.bot1.num + 1) + ") map:"
                    self.bot1.map.show_map()
                    print "\n" + self.bot2.name + " (" + str(self.bot2.num + 1) + ") map:"
                    self.bot2.map.show_map()
                    print "\nWin bot %d\n" % (winner.num + 1)
                    self.wins[winner.num] += 1

                    self.lock.acquire()
                    winlist[0] = self.wins[0]
                    winlist[1] = self.wins[1]
                    winlist[2] += 1
                    self.lock.release()

                else:
                    print "Game don't played"
                time.sleep(self.game_pause)
            else:
                raise Exception("End of thread")

        print 'Bot 1: %d \nBot 2: %d ' % (self.wins[0], self.wins[1])

    def __del__(self):
        if self.bot1:
            self.bot1.__del__()
        if self.bot2:
            self.bot2.__del__()


if __name__ == '__main__':
    j = Judge("./shooted.bmp", "./bot.py")
    j.play_championship(10)
