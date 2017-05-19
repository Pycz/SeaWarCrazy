#!/usr/bin/env python

#from subprocess import Popen, PIPE
import fcntl, select, os
import pty, sys, signal, select

#p1 = Popen(["./test.py"], shell = True, stdout=PIPE, stdin = PIPE)
#p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
#p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
#fcntl.fcntl(p1.stdout.fileno(), fcntl.F_SETFL, fcntl.fcntl(p1.stdout.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)
'''
pty.spawn("./test.py")
test_in = sys.stdout

test_out = sys.stdin

sys.stdout = sys.__stdout__
sys.stdin = sys.__stdin__
'''
temp_pid, temp_fd = pty.fork()

if temp_pid == 0:
    os.execl("./test.py", "./test.py")


'''
s = ''

temp_fd = select.select([temp_fd, ], [], [])[0][0]
s += os.read(temp_fd, 3).strip()
print s

temp_fd = select.select([temp_fd, ], [], [])[0][0]
s += os.read(temp_fd, 3).strip()
print s

os.write(temp_fd, "H\n")
temp_fd = select.select([temp_fd, ], [], [])[0][0]
os.read(temp_fd, 3)

temp_fd = select.select([temp_fd, ], [], [])[0][0]
s += os.read(temp_fd, 3).strip()
print s

temp_fd = select.select([temp_fd, ], [], [])[0][0]
s += os.read(temp_fd, 3).strip()
print s

temp_fd = select.select([temp_fd, ], [], [])[0][0]
s += os.read(temp_fd, 3).strip()
print s

temp_fd = select.select([temp_fd, ], [], [])[0][0]
s += os.read(temp_fd, 3).strip()
print s

print repr(s)
'''


test_in = os.fdopen(temp_fd, "r", 0)
test_out = os.fdopen(temp_fd, "w", 0)

print test_in.readline().strip()
print test_in.readline().strip()
test_out.write("H\n")
test_in.readline()
print test_in.readline().strip()
print test_in.readline().strip()
print test_in.readline().strip()
print test_in.readline().strip()
#print test_in.readline()
try:
    test_in.close()
except:
    pass

try:
    test_out.close()
except:
    pass


try:
    os.kill(temp_pid, signal.SIGTERM)
except:
    pass

'''
output = p1.stdout.readline()
print output
output = p1.stdout.readline()
print output
p1.stdin.write("Hello!\n")
output = p1.stdout.readline()
print output
p1.kill()'''
