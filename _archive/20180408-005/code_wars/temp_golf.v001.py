import sys
import math
c = 2
l = [-4, 5]
try:
    # c = int(input())
    # l = [int(t) for t in input().split()]
    #n = [t for t in l if t < 0]
    o = min(l, key = abs)
    #o = m if len(n) == len(l) else abs(m)
except:
    o = 0
print (o)
