import sys
import math
import numpy

# Save humans, destroy zombies!


# game loop
while True:
    x, y = [int(i) for i in input().split()]
    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Your destination coordinates
    if zombie_count > 0:
        z_curr_dist = (math.hypot(abs(zombie_x - human_x), abs(zombie_y - human_y)))
        z_next_dist = (math.hypot(abs(zombie_xnext - human_x), abs(zombie_ynext - human_y)))
        if human_count <= 2:
            print ( human_x, human_y )
        elif z_curr_dist > z_next_dist:
            print ( int(numpy.mean( [zombie_x, human_x] ) ), int( numpy.mean( [zombie_y, human_y] ) ) )
        else:
            print ( int(numpy.mean( [zombie_xnext, human_x] ) ), int( numpy.mean( [zombie_ynext, human_y] ) ) )


        # print (abs(human_x - zombie_x), abs(human_y - zombie_y))
