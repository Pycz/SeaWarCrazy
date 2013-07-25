#!/usr/bin/python
'''
Created on 20.07.2013

@author: pycz
'''
import sys, time
#time.sleep(1)
sys.stdout.write('1\n')
#time.sleep(1)
sys.stdout.write('2\n')
#time.sleep(1)
#sys.stdout.flush()
x = 0
x = sys.stdin.readline().strip()
#sys.stdout.flush()
#time.sleep(1)
sys.stdout.write(chr(ord(str(x))+1) + '\n')
#time.sleep(1)
sys.stdout.write('4\n')
#time.sleep(1)
sys.stdout.write('5\n')
#time.sleep(1)
sys.stdout.write('6\n')
#time.sleep(3)
