import sys
import math
import numpy

# Don't let the machines win. You are humanity's last hope...

width = int(input())  # the number of cells on the X axis
height = int(input())  # the number of cells on the Y axis
sys.stderr.write( str("width: %s \n" ) % ( str(width) ) )
sys.stderr.write( str("height: %s \n" ) % ( str(height) ) )

gridCoord_list = [ (x, y) for x in range(width) for y in range(height)]
dot_list = [ list(input()) for h in range(height) ]
grid_matrix = numpy.matrix( dot_list )
sys.stderr.write( str("gridCoord_list: %s \n" ) % ( str(gridCoord_list) ) )
sys.stderr.write( str("dot_list: %s \n" ) % ( str(dot_list) ) )
sys.stderr.write( str("grid_matrix: %s \n" ) % ( str(grid_matrix) ) )


# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)


# Three coordinates: a node, its right neighbor, its bottom neighbor
print("0 0 1 0 0 1")
