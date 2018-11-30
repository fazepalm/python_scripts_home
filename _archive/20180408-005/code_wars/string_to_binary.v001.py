import sys
import math
import binascii

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

message = input()


# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)



prev_val = 0
bin_out = []


bin_list = ''.join(format(x, 'b') for x in bytearray(message, 'UTF-8'))

for val in bin_list:
    f_block = None
    if val != prev_val:
        if int(val) == 1:
            f_block = ' 0 '

            #print block_1
        if int(val) == 0:
             f_block = ' 00 '
            #print block_0
    if f_block != None:
        bin_out.append( f_block )
    bin_out.append( val )

    prev_val = val

print ( ''.join( bin_out ).replace( str(1), str(0) ).lstrip( ' ' ) )
