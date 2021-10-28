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
parser.add_argument("--inputdir", help="Specify the main directory for the G-spinor basis set", required=False,
            type=str, default="./")
parser.add_argument("-An","--automatic_genAn", help="Specify the n integer in the automatic algorithm fitting basiis set generation 2 (default) 3  4 ", required=True,
            type=int, default=2)
parser.add_argument("--add_diffuse", help="Specify add an extra exponent in the series (default)", required=False, default=False, action="store_true")



args = parser.parse_args()
print("Options: ")
print(args)
print("")
print("")

inputdir = args.inputdir

gspinorbasis = args.inputfile
n = args.automatic_genAn

print(args.inputfile)
print(args.automatic_genAn)
print(gspinorbasis)
filebasis = inputdir+gspinorbasis

if not os.path.isfile(filebasis):
    print("File ", filebasis, " does not exist")
    exit(1)


with open(filebasis,"r") as fp:
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

if args.add_diffuse:	
   for i in range(N-2):
      bn = bn/(6-n)
      beta.append(bn) 

      filefittingbasis = gspinorbasis[:-4]+"_autoGENA"+str(n)+"spd+.txt"
      outep = open(filefittingbasis, "w")
      outep.write ("%4i \n"%(N+1))
   for i in range(N+1):
        outep.write ("%10.5f 2 \n"%beta[i])
     
   outep.write ("# File generated from repository" +filebasis)
   outep.write ("\n")
   outep.write ("# using the Demon Style see the Demon Manual \n")
   outep.write ("# koster et al. \n")
   outep.write ("# One diffuse function has been added \n")


if not args.add_diffuse:    
   for i in range(N-3):
      bn = bn/(6-n)
      beta.append(bn)

      filefittingbasis = gspinorbasis[:-4]+"_autoGENA"+str(n)+"spd.txt"
      outep = open(filefittingbasis, "w")
      outep.write ("%4i \n"%(N))
   for i in range(N):
        outep.write ("%10.5f 2 \n"%beta[i])

   outep.write ("# File generated from repository" +filebasis)
   outep.write ("\n")
   outep.write ("# using the Demon Style see the Demon Manual \n")
   outep.write ("# koster et al. \n")
   print(beta)

