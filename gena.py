import argparse 
import os 
import sys
import math
import numpy as np
"""
Automatic Generation of Auxiliary Functions
Taken form the Demon Manual Need to be tested
Generate spd 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f","--inputfile", help="Specify the G-spinor basis set", required=True,
            type=str, default="aug-cc-pvtz.txt")


args = parser.parse_args()
print("Options: ")
print(args)
print("")
print("")

gspinorbasis = args.inputfile

print(args.inputfile)
print(gspinorbasis)

if not os.path.isfile(gspinorbasis):
    print("File ", gspinorbasis, " does not exist")
    exit(1)


with open(gspinorbasis,"r") as fp:
    Lines = fp.readlines()    
    count = 0
    maxl = int(Lines[count])
    count = count + 1
    explist = []

    for i in range(maxl+1):
            nexpl = int(Lines[count]) 
            count = count + 1
            for j in range(nexpl):
               explist.append(float(Lines[count])) 
               count = count + 1

fp.close()

print("explist")
print(*explist)
arr = np.array(explist)
print(arr)

n = 4 
bmax = np.max(arr)
bmin = np.min(arr) 
print(bmax,bmin)

N = int((math.log(bmax/bmin)/math.log(6-n))+0.5)

print(N)

b0 = 2*bmin*(6-n)**(N-1)

print(b0)

b1 = (1+n/(12-2*n))*b0
b2 = b0/(6-n)

beta = []
beta.append(b0)
beta.append(b1)
beta.append(b2)

bn = b2

for i in range(N-3):
   bn = bn/(6-n)
   beta.append(bn) 

outep = open(gspinorbasis+"GENA"+str(n), "w")
outep.write ("%4i \n"%N)
for i in range(N-1):
     outep.write ("%10.5f 2 \n"%beta[i])

