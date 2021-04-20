import sys
import re

###################################################################

def is_float(s):

    try:
        width = float(s)
    except ValueError:
        return False

    return True

###################################################################

fname = ""
atname = "Au"

if len(sys.argv) == 2:
    fname = sys.argv[1]
else:
    print "usage: ", sys.argv[0] , " inpufile.txt "
    exit(1)

fp = open(fname)

allfile = []

for l in fp:
    p = re.compile(r'\s+')
    line = p.sub(' ', l)
    line = line.lstrip()
    line = line.rstrip()

    allfile.append(line)

fp.close()

extracted = []
startparsing = False
for line in allfile:

    if startparsing:

        if not (line.strip() == ""):
            firstchar = line.strip()[0]
            if (firstchar.isdigit()):
                extracted.append(line)

        if line.find ("Small component functions") != -1:
            break

    if line.find ("** "+ atname) != -1:
        startparsing = True

# forse un dizionario in cui classifico anche per momento
# angolare 
set_of_list = []
subset = [] 

for line in extracted:
    sline = line.split(" ")
    if is_float(sline[0]):
        subset.append(sline)
    else:
        set_of_list.append(subset)
        subset = []

for subset in set_of_list:
    if len(subset) != 0:
        print len(subset)
        for line in subset:
            print line[1]

# servono si no ? sarebbe il caso di fare qualche test
# qui abbiamo altre f o g o h o dipende dai casi vanno
# aggiunte solo se non repsenti 
print "extra func"
for line in allfile:
    sline = line.split(" ")
    if len(sline) >= 2:
        if sline[0] == "Au":
            for i in range(1,len(sline)):
                print sline[i]

""" dump all
for subset in set_of_list:
    if len(subset) != 0:
        for line in subset:
            print line
"""
