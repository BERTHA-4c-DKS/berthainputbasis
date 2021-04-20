import os
import re
import sys
import numpy

if len(sys.argv) <= 2:
  print "need to specify at least 2 bertha output files"
  exit(1)

spenergy = []

for i in range(1, len(sys.argv)):
  if not (os.path.isfile(sys.argv[i])):
    print("File " + sys.argv[i] + " does not exist ")
    exit(1)

  fp = open(sys.argv[i])
  energy = []

  for line in fp:
    if line.startswith(" total energy ="):
      p = re.compile(r'\s+')
      line = p.sub(' ', line)
      line = line.lstrip()
      line = line.rstrip()
      
      sline = line.split(" ")
      if len(sline) != 4:
        print "error in parsing file ", sys.argv[i]
        exit(1)

      energy.append(numpy.float64(sline[3]))

  fp.close()

  if len(energy) < 1:
    print "no energy, error in parsing file ", sys.argv[i]
    exit(1)

  spenergy.append(energy[-1])

for spe in spenergy:
  print spe
