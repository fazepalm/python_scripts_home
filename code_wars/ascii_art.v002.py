import sys
import math
import string
import re
from collections import defaultdict

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
alpha_list = list(string.ascii_uppercase)
alpha_list.append( '?' )
alpha_dict = {}
ascii_dict = defaultdict(list)

l = int(input())
h = int(input())
t = input()

for a_count, alpha in enumerate(alpha_list):
    alpha_dict[alpha] = a_count

split_count = 0

for i in range(h):
    input_line = input()
    input_split = list(filter(None, re.split(r'(\W{1}|\s{1})', input_line)))

    for input_count in range(int(len(input_split) / (int(l)))):
        split_count = input_count * 4
        chr_line = (input_split[split_count:int(l) + split_count])

        ascii_dict[input_count].append(chr_line)
        # if input_count == 26:
        #     sys.stderr.write( str("chr_line: %s \n" ) % ( str(chr_line) ) )

chr_out_list = []
for out_chr in t:
    out_chr = out_chr.upper()

    lookup_index = alpha_dict.get( out_chr )
    r_ascii_list = ascii_dict[lookup_index]
    for ascii_line in r_ascii_list:
        chr_out = ''.join(ascii_line)
        sys.stderr.write( str("chr_out: %s \n" ) % ( str(chr_out) ) )
        print (chr_out)
        chr_out_list.append(chr_out)
#sys.stderr.write( str("chr_out_list: %s \n" ) % ( str(chr_out_list) ) )
