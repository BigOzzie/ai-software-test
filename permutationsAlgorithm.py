import sys
from itertools import permutations

if len(sys.argv) < 2:
    raise Exception("No filename was supplied")

filename = sys.argv[1]
try:
    f = open(filename,"r")
except FileNotFoundError:
    print("Invalid filename: "+ filename)
else:
    for line in f.readlines():
        if line[-1] == '\n': line = line[:-1]
        output = [''.join(p) for p in permutations(line)]
        output.sort()
        output = ','.join(output)
        sys.stdout.write(output + '\n')
    f.close()