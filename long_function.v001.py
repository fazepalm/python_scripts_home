import sys
def longfunction():
  for i in rrange(0, 100000):
     sys.stdout.write("Result Output: %s" % (str(i)))

if __name__ == '__main__':
    longfunction()
