import sys
from subprocess import PIPE, Popen
from threading  import Thread

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # python 2.x

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

p = Popen(['C:/Program Files/Autodesk/Maya2018/bin/maya.exe'], stdout=PIPE, bufsize=1)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

# ... do other things here

# read line without blockin
# while Empty:
#     print "no output"
#
# line = q.get_nowait()
# print (line)
try:
    line = q.get_nowait() # or q.get(timeout=.1)
except Empty:
    print('no output yet')
else: # got line
    print line
